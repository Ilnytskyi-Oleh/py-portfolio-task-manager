import re

from django import forms
from django.utils.translation import gettext_lazy as _

from tasks.models import Project, Tag, Task, TaskType, Team, Worker
from tasks.permissions import is_staff_user

_TAG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def projects_for_user(user: Worker):
    if is_staff_user(user):
        return Project.objects.all()
    return Project.objects.filter(team__members=user).distinct()


def teams_for_user(user: Worker):
    if is_staff_user(user):
        return Team.objects.all()
    return user.teams.all()


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        required=False,
        label=_("Assignees"),
        widget=forms.CheckboxSelectMultiple,
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label=_("Tags"),
        widget=forms.CheckboxSelectMultiple,
    )
    tag_names = forms.CharField(
        required=False,
        label=_("New tags"),
        help_text=_("Comma-separated new tags (e.g. python-refactoring)"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "landing-page-layout, api",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "project",
            "assignees",
            "tags",
            "is_completed",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "deadline": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 4, "class": "form-control"}
            ),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "task_type": forms.Select(attrs={"class": "form-select"}),
            "project": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, user=None, **kwargs) -> None:
        self.user = user
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["project"].queryset = projects_for_user(user)

    def clean_tag_names(self) -> str:
        raw = self.cleaned_data.get("tag_names", "")
        if not raw:
            return ""
        invalid = []
        for part in raw.split(","):
            name = part.strip().lower().replace(" ", "-")
            if not name:
                continue
            if not _TAG_RE.match(name) or len(name) > 64:
                invalid.append(part.strip())
        if invalid:
            raise forms.ValidationError(
                _(
                    "Invalid tags: %(tags)s. Use lowercase letters, "
                    "digits and hyphens only."
                ),
                params={"tags": ", ".join(invalid)},
            )
        return raw

    def clean_project(self) -> Project:
        project = self.cleaned_data["project"]
        if (
            self.user is not None
            and not projects_for_user(self.user)
            .filter(pk=project.pk)
            .exists()
        ):
            raise forms.ValidationError(
                _("You cannot create tasks in this project.")
            )
        return project

    def save(self, commit: bool = True) -> Task:
        task = super().save(commit=False)
        if commit:
            task.save()
            self.save_m2m()
            self._attach_new_tags(task)
        return task

    def _attach_new_tags(self, task: Task) -> None:
        raw = self.cleaned_data.get("tag_names", "")
        if not raw:
            return
        for part in raw.split(","):
            name = part.strip().lower().replace(" ", "-")
            if not name or not _TAG_RE.match(name):
                continue
            tag, _ = Tag.objects.get_or_create(name=name)
            task.tags.add(tag)


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Search by name"),
                "class": "form-control",
            }
        ),
    )
    status = forms.ChoiceField(
        required=False,
        choices=(
            ("", _("All statuses")),
            ("open", _("Open")),
            ("done", _("Completed")),
        ),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    priority = forms.ChoiceField(
        required=False,
        choices=[("", _("All priorities"))] + list(Task.Priority.choices),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        empty_label=_("All projects"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        empty_label=_("All tags"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        required=False,
        empty_label=_("All teams"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class TeamForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        required=False,
        label=_("Members"),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Team
        fields = ("name", "members")


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description", "team")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
            "team": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, user=None, **kwargs) -> None:
        self.user = user
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["team"].queryset = teams_for_user(user)

    def clean_team(self) -> Team:
        team = self.cleaned_data["team"]
        if (
            self.user is not None
            and not teams_for_user(self.user).filter(pk=team.pk).exists()
        ):
            raise forms.ValidationError(
                _("You cannot manage projects for this team.")
            )
        return team


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Search by username"),
                "class": "form-control",
            }
        ),
    )


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ("name",)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name",)

    def clean_name(self) -> str:
        name = self.cleaned_data["name"].strip().lower().replace(" ", "-")
        if not _TAG_RE.match(name):
            raise forms.ValidationError(
                _("Use lowercase letters, digits and hyphens only.")
            )
        return name
