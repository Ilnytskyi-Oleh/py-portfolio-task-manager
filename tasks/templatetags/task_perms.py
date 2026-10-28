from django import template
from django.conf import settings

from tasks.permissions import (
    can_manage_project as _can_manage_project,
    can_manage_task as _can_manage_task,
    can_manage_team as _can_manage_team,
)

register = template.Library()


@register.filter
def can_manage_task(user, task) -> bool:
    return _can_manage_task(user, task)


@register.filter
def can_manage_project(user, project) -> bool:
    return _can_manage_project(user, project)


@register.filter
def can_manage_team(user, team) -> bool:
    return _can_manage_team(user, team)


@register.simple_tag
def demo_mode() -> bool:
    return bool(settings.DEBUG)
