from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import (
    Case,
    Count,
    IntegerField,
    Q,
    QuerySet,
    Value,
    When,
)
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import (
    ProjectForm,
    TagForm,
    TaskForm,
    TaskSearchForm,
    TaskTypeForm,
    TeamForm,
    WorkerSearchForm,
)
from tasks.models import Project, Tag, Task, TaskType, Team, Worker
from tasks.permissions import (
    ProjectManagePermissionMixin,
    StaffRequiredMixin,
    TaskManagePermissionMixin,
    TeamManagePermissionMixin,
    can_manage_project,
    require_can_manage_task,
)


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "tasks/index.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        my_tasks = user.assigned_tasks.all()
        context.update(
            {
                "num_workers": Worker.objects.count(),
                "num_teams": Team.objects.count(),
                "num_projects": Project.objects.count(),
                "num_tasks": Task.objects.count(),
                "my_open_tasks": my_tasks.filter(is_completed=False).count(),
                "my_done_tasks": my_tasks.filter(is_completed=True).count(),
            }
        )
        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10
    template_name = "tasks/task_list.html"
    context_object_name = "task_list"
    sort_fields = {
        "name": "name",
        "deadline": "deadline",
        "status": "is_completed",
        "project": "project__name",
        "priority": "priority_rank",
    }

    def _current_sort(self) -> str:
        sort = self.request.GET.get("sort", "deadline")
        if sort not in self.sort_fields:
            return "deadline"
        return sort

    def _current_dir(self) -> str:
        direction = self.request.GET.get("dir", "asc")
        if direction not in {"asc", "desc"}:
            return "asc"
        return direction

    def get_queryset(self) -> QuerySet:
        queryset = Task.objects.select_related(
            "task_type",
            "project",
            "project__team",
            "creator",
        ).prefetch_related("assignees", "tags").annotate(
            priority_rank=Case(
                When(priority=Task.Priority.URGENT, then=Value(0)),
                When(priority=Task.Priority.HIGH, then=Value(1)),
                When(priority=Task.Priority.MEDIUM, then=Value(2)),
                When(priority=Task.Priority.LOW, then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            )
        )

        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            if name:
                queryset = queryset.filter(name__icontains=name)

            status = form.cleaned_data.get("status")
            if status == "open":
                queryset = queryset.filter(is_completed=False)
            elif status == "done":
                queryset = queryset.filter(is_completed=True)

            priority = form.cleaned_data.get("priority")
            if priority:
                queryset = queryset.filter(priority=priority)

            project = form.cleaned_data.get("project")
            if project:
                queryset = queryset.filter(project=project)

            tag = form.cleaned_data.get("tag")
            if tag:
                queryset = queryset.filter(tags=tag)

            team = form.cleaned_data.get("team")
            if team:
                queryset = queryset.filter(project__team=team)

        sort_key = self.sort_fields[self._current_sort()]
        if self._current_dir() == "desc":
            sort_key = f"-{sort_key}"
        return queryset.distinct().order_by(sort_key, "name")

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskSearchForm(self.request.GET)
        context["current_sort"] = self._current_sort()
        context["current_dir"] = self._current_dir()
        context["today"] = date.today()
        context["status_filter"] = self.request.GET.get("status", "")
        return context


class MyTaskListView(TaskListView):
    template_name = "tasks/my_task_list.html"

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(assignees=self.request.user)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "tasks/task_detail.html"

    def get_queryset(self) -> QuerySet:
        return Task.objects.select_related(
            "task_type",
            "project",
            "project__team",
            "creator",
        ).prefetch_related("assignees", "tags")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task-list")

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form: TaskForm) -> HttpResponse:
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskUpdateView(
    LoginRequiredMixin,
    TaskManagePermissionMixin,
    generic.UpdateView,
):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskDeleteView(
    LoginRequiredMixin,
    TaskManagePermissionMixin,
    generic.DeleteView,
):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task-list")


@login_required
def toggle_task_complete(
    request: HttpRequest,
    pk: int,
) -> HttpResponse:
    task = get_object_or_404(
        Task.objects.select_related("project__team"),
        pk=pk,
    )
    require_can_manage_task(request.user, task)
    if request.method == "POST":
        task.is_completed = not task.is_completed
        task.save(update_fields=["is_completed"])
    return redirect(task.get_absolute_url())


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 10
    template_name = "tasks/worker_list.html"
    context_object_name = "worker_list"

    def get_queryset(self) -> QuerySet:
        queryset = Worker.objects.select_related("position").annotate(
            open_tasks=Count(
                "assigned_tasks",
                filter=Q(assigned_tasks__is_completed=False),
            ),
            done_tasks=Count(
                "assigned_tasks",
                filter=Q(assigned_tasks__is_completed=True),
            ),
        )
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            if username:
                queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["search_form"] = WorkerSearchForm(self.request.GET)
        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "tasks/worker_detail.html"

    def get_queryset(self) -> QuerySet:
        return Worker.objects.select_related("position").prefetch_related(
            "teams",
            "assigned_tasks__project",
            "assigned_tasks__tags",
            "assigned_tasks__task_type",
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        assigned = self.object.assigned_tasks.all()
        context["completed_tasks"] = assigned.filter(is_completed=True)
        context["incomplete_tasks"] = assigned.filter(is_completed=False)
        return context


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 10
    template_name = "tasks/team_list.html"
    context_object_name = "team_list"

    def get_queryset(self) -> QuerySet:
        return Team.objects.annotate(
            member_count=Count("members", distinct=True),
            project_count=Count("projects", distinct=True),
        )


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    template_name = "tasks/team_detail.html"

    def get_queryset(self) -> QuerySet:
        return Team.objects.prefetch_related(
            "members__position",
            "projects",
        )


class TeamCreateView(
    LoginRequiredMixin,
    TeamManagePermissionMixin,
    generic.CreateView,
):
    model = Team
    form_class = TeamForm
    template_name = "tasks/team_form.html"
    success_url = reverse_lazy("tasks:team-list")


class TeamUpdateView(
    LoginRequiredMixin,
    TeamManagePermissionMixin,
    generic.UpdateView,
):
    model = Team
    form_class = TeamForm
    template_name = "tasks/team_form.html"


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 10
    template_name = "tasks/project_list.html"
    context_object_name = "project_list"

    def get_queryset(self) -> QuerySet:
        return Project.objects.select_related("team").annotate(
            task_count=Count("tasks"),
        )


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    template_name = "tasks/project_detail.html"

    def get_queryset(self) -> QuerySet:
        return Project.objects.select_related("team").prefetch_related(
            "tasks__assignees",
            "tasks__tags",
            "tasks__task_type",
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["today"] = date.today()
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "tasks/project_form.html"
    success_url = reverse_lazy("tasks:project-list")

    def dispatch(self, request, *args, **kwargs):
        if not can_manage_project(request.user):
            raise PermissionDenied("You cannot create projects.")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ProjectUpdateView(
    LoginRequiredMixin,
    ProjectManagePermissionMixin,
    generic.UpdateView,
):
    model = Project
    form_class = ProjectForm
    template_name = "tasks/project_form.html"

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "tasks/task_type_list.html"
    context_object_name = "task_type_list"


class TaskTypeCreateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    generic.CreateView,
):
    model = TaskType
    form_class = TaskTypeForm
    template_name = "tasks/task_type_form.html"
    success_url = reverse_lazy("tasks:task-type-list")


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    template_name = "tasks/tag_list.html"
    context_object_name = "tag_list"

    def get_queryset(self) -> QuerySet:
        return Tag.objects.annotate(task_count=Count("tasks"))


class TagCreateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    generic.CreateView,
):
    model = Tag
    form_class = TagForm
    template_name = "tasks/tag_form.html"
    success_url = reverse_lazy("tasks:tag-list")
