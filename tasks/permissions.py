from __future__ import annotations

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

from tasks.models import Project, Task, Team, Worker


def is_staff_user(user: Worker) -> bool:
    return bool(user.is_authenticated and user.is_staff)


def is_team_member(user: Worker, team: Team) -> bool:
    if not user.is_authenticated:
        return False
    return team.members.filter(pk=user.pk).exists()


def can_manage_task(user: Worker, task: Task) -> bool:
    if not user.is_authenticated:
        return False
    if is_staff_user(user):
        return True
    if task.creator_id == user.pk:
        return True
    if task.assignees.filter(pk=user.pk).exists():
        return True
    return is_team_member(user, task.project.team)


def can_manage_team(user: Worker, team: Team | None = None) -> bool:
    return is_staff_user(user)


def can_manage_project(user: Worker, project: Project | None = None) -> bool:
    if not user.is_authenticated:
        return False
    if is_staff_user(user):
        return True
    if project is None:
        return user.teams.exists()
    return is_team_member(user, project.team)


def can_manage_taxonomy(user: Worker) -> bool:
    return is_staff_user(user)


def require_can_manage_task(user: Worker, task: Task) -> None:
    if not can_manage_task(user, task):
        raise PermissionDenied("You cannot modify this task.")


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return is_staff_user(self.request.user)


class TaskManagePermissionMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        task = self.get_object()
        return can_manage_task(self.request.user, task)


class TeamManagePermissionMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return can_manage_team(self.request.user)


class ProjectManagePermissionMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return can_manage_project(self.request.user, self.get_object())


def client_ip(request: HttpRequest) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")
