from django.urls import path

from tasks import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path("tasks/my/", views.MyTaskListView.as_view(), name="my-task-list"),
    path(
        "tasks/create/",
        views.TaskCreateView.as_view(),
        name="task-create",
    ),
    path(
        "tasks/<int:pk>/",
        views.TaskDetailView.as_view(),
        name="task-detail",
    ),
    path(
        "tasks/<int:pk>/update/",
        views.TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "tasks/<int:pk>/delete/",
        views.TaskDeleteView.as_view(),
        name="task-delete",
    ),
    path(
        "tasks/<int:pk>/toggle-complete/",
        views.toggle_task_complete,
        name="task-toggle-complete",
    ),
    path("workers/", views.WorkerListView.as_view(), name="worker-list"),
    path(
        "workers/<int:pk>/",
        views.WorkerDetailView.as_view(),
        name="worker-detail",
    ),
    path("teams/", views.TeamListView.as_view(), name="team-list"),
    path(
        "teams/create/",
        views.TeamCreateView.as_view(),
        name="team-create",
    ),
    path(
        "teams/<int:pk>/",
        views.TeamDetailView.as_view(),
        name="team-detail",
    ),
    path(
        "teams/<int:pk>/update/",
        views.TeamUpdateView.as_view(),
        name="team-update",
    ),
    path("projects/", views.ProjectListView.as_view(), name="project-list"),
    path(
        "projects/create/",
        views.ProjectCreateView.as_view(),
        name="project-create",
    ),
    path(
        "projects/<int:pk>/",
        views.ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "projects/<int:pk>/update/",
        views.ProjectUpdateView.as_view(),
        name="project-update",
    ),
    path(
        "task-types/",
        views.TaskTypeListView.as_view(),
        name="task-type-list",
    ),
    path(
        "task-types/create/",
        views.TaskTypeCreateView.as_view(),
        name="task-type-create",
    ),
    path("tags/", views.TagListView.as_view(), name="tag-list"),
    path("tags/create/", views.TagCreateView.as_view(), name="tag-create"),
]

app_name = "tasks"
