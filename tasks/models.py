from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("position")
        verbose_name_plural = _("positions")

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workers",
        verbose_name=_("position"),
    )

    class Meta:
        ordering = ["username"]
        verbose_name = _("worker")
        verbose_name_plural = _("workers")

    def __str__(self) -> str:
        full_name = self.get_full_name()
        if full_name:
            return f"{self.username} ({full_name})"
        return self.username

    def get_absolute_url(self) -> str:
        return reverse("tasks:worker-detail", kwargs={"pk": self.pk})


class Team(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=True)
    members = models.ManyToManyField(
        Worker,
        related_name="teams",
        blank=True,
        verbose_name=_("members"),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("team")
        verbose_name_plural = _("teams")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("tasks:team-detail", kwargs={"pk": self.pk})


class Project(models.Model):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name=_("team"),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("tasks:project-detail", kwargs={"pk": self.pk})


class TaskType(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("task type")
        verbose_name_plural = _("task types")

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "urgent", _("Urgent")
        HIGH = "high", _("High")
        MEDIUM = "medium", _("Medium")
        LOW = "low", _("Low")

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    deadline = models.DateField(_("deadline"), null=True, blank=True)
    is_completed = models.BooleanField(_("completed"), default=False)
    priority = models.CharField(
        _("priority"),
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.PROTECT,
        related_name="tasks",
        verbose_name=_("task type"),
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name=_("project"),
    )
    creator = models.ForeignKey(
        Worker,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_tasks",
        verbose_name=_("creator"),
    )
    assignees = models.ManyToManyField(
        Worker,
        related_name="assigned_tasks",
        blank=True,
        verbose_name=_("assignees"),
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tasks",
        blank=True,
        verbose_name=_("tags"),
    )

    class Meta:
        ordering = ["is_completed", "deadline", "name"]
        verbose_name = _("task")
        verbose_name_plural = _("tasks")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("tasks:task-detail", kwargs={"pk": self.pk})
