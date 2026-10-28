from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import (
    Position,
    Project,
    Tag,
    Task,
    TaskType,
    Team,
    Worker,
)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "position",
                ),
            },
        ),
    )
    list_filter = UserAdmin.list_filter + ("position",)
    search_fields = ("username", "first_name", "last_name", "email")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("members",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "team")
    list_filter = ("team",)
    search_fields = ("name",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "project",
        "task_type",
        "priority",
        "deadline",
        "is_completed",
        "creator",
    )
    list_filter = (
        "is_completed",
        "priority",
        "task_type",
        "project",
        "tags",
    )
    search_fields = ("name", "description")
    filter_horizontal = ("assignees", "tags")
    autocomplete_fields = ("project", "task_type", "creator")
