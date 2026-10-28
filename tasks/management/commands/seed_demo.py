from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from tasks.models import (
    Position,
    Project,
    Tag,
    Task,
    TaskType,
    Team,
    Worker,
)


class Command(BaseCommand):
    # Django BaseCommand API uses attribute name "help".
    help = (  # noqa: VNE003
        "Load demo positions, workers, teams, projects and tasks"
    )

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        positions = {
            name: Position.objects.get_or_create(name=name)[0]
            for name in (
                "Developer",
                "Project Manager",
                "QA",
                "Designer",
                "DevOps",
            )
        }

        task_types = {
            name: TaskType.objects.get_or_create(name=name)[0]
            for name in (
                "Bug",
                "New feature",
                "Breaking change",
                "Refactoring",
                "QA",
            )
        }

        tags = {
            name: Tag.objects.get_or_create(name=name)[0]
            for name in (
                "landing-page-layout",
                "python-refactoring",
                "auth",
                "api",
            )
        }

        admin, created = Worker.objects.get_or_create(
            username="admin.user",
            defaults={
                "email": "admin@example.com",
                "first_name": "Ada",
                "last_name": "Admin",
                "position": positions["Project Manager"],
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin.set_password("1qazcde3")
            admin.save()

        workers_data = [
            ("dev.anna", "Anna", "Dev", "Developer"),
            ("qa.oleg", "Oleg", "QA", "QA"),
            ("design.ira", "Ira", "Design", "Designer"),
            ("ops.max", "Max", "Ops", "DevOps"),
        ]
        workers = {"admin.user": admin}
        for username, first, last, position_name in workers_data:
            worker, created = Worker.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                    "first_name": first,
                    "last_name": last,
                    "position": positions[position_name],
                },
            )
            if created:
                worker.set_password("1qazcde3")
                worker.save()
            workers[username] = worker

        frontend, _ = Team.objects.get_or_create(name="Frontend Squad")
        backend, _ = Team.objects.get_or_create(name="Backend Squad")
        frontend.members.set(
            [workers["dev.anna"], workers["design.ira"], workers["qa.oleg"]]
        )
        backend.members.set(
            [workers["dev.anna"], workers["ops.max"], admin]
        )

        vacancies, _ = Project.objects.get_or_create(
            name="Vacancies Portal",
            defaults={
                "description": "Public vacancies dashboard and forms",
                "team": frontend,
            },
        )
        auth_proj, _ = Project.objects.get_or_create(
            name="Auth Platform",
            defaults={
                "description": "Sign-in and identity services",
                "team": backend,
            },
        )

        today = date.today()
        task_specs = [
            {
                "name": "Fix Dashboard for Vacancies",
                "description": "Layout breaks on tablet width.",
                "deadline": today + timedelta(days=3),
                "priority": Task.Priority.URGENT,
                "task_type": task_types["Bug"],
                "project": vacancies,
                "creator": admin,
                "assignees": [workers["dev.anna"], workers["design.ira"]],
                "tags": [tags["landing-page-layout"]],
                "is_completed": False,
            },
            {
                "name": "Add sign-in with Google button",
                "description": "OAuth button on login page.",
                "deadline": today + timedelta(days=7),
                "priority": Task.Priority.HIGH,
                "task_type": task_types["New feature"],
                "project": auth_proj,
                "creator": workers["dev.anna"],
                "assignees": [workers["dev.anna"], workers["ops.max"]],
                "tags": [tags["auth"], tags["api"]],
                "is_completed": False,
            },
            {
                "name": "Refactor task serializers",
                "description": "Clean up duplicated validation.",
                "deadline": today - timedelta(days=1),
                "priority": Task.Priority.MEDIUM,
                "task_type": task_types["Refactoring"],
                "project": auth_proj,
                "creator": admin,
                "assignees": [workers["dev.anna"]],
                "tags": [tags["python-refactoring"]],
                "is_completed": True,
            },
            {
                "name": "Smoke test vacancies flow",
                "description": "Cover create/edit vacancy paths.",
                "deadline": today + timedelta(days=5),
                "priority": Task.Priority.LOW,
                "task_type": task_types["QA"],
                "project": vacancies,
                "creator": workers["qa.oleg"],
                "assignees": [workers["qa.oleg"]],
                "tags": [tags["landing-page-layout"]],
                "is_completed": False,
            },
        ]

        for spec in task_specs:
            assignees = spec.pop("assignees")
            tag_list = spec.pop("tags")
            task, created = Task.objects.get_or_create(
                name=spec["name"],
                project=spec["project"],
                defaults=spec,
            )
            if created:
                task.assignees.set(assignees)
                task.tags.set(tag_list)

        self.stdout.write(self.style.SUCCESS("Demo data loaded."))
