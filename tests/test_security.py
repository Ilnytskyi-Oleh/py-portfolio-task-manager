from datetime import date

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from tasks.models import Position, Project, Task, TaskType, Team

Worker = get_user_model()


class AuthorizationTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        position = Position.objects.create(name="Developer")
        self.owner = Worker.objects.create_user(
            username="owner",
            password="pass12345",
            position=position,
        )
        self.outsider = Worker.objects.create_user(
            username="outsider",
            password="pass12345",
            position=position,
        )
        self.staff = Worker.objects.create_user(
            username="staff.user",
            password="pass12345",
            position=position,
            is_staff=True,
        )
        self.team = Team.objects.create(name="Alpha")
        self.team.members.add(self.owner)
        self.project = Project.objects.create(name="App", team=self.team)
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Secure task",
            deadline=date.today(),
            task_type=self.task_type,
            project=self.project,
            creator=self.owner,
        )
        self.task.assignees.add(self.owner)

    def test_outsider_cannot_update_task(self) -> None:
        self.client.force_login(self.outsider)
        response = self.client.post(
            reverse("tasks:task-update", kwargs={"pk": self.task.pk}),
            data={
                "name": "Hacked",
                "description": "",
                "deadline": date.today().isoformat(),
                "priority": Task.Priority.LOW,
                "task_type": self.task_type.pk,
                "project": self.project.pk,
                "is_completed": True,
            },
        )
        self.assertEqual(response.status_code, 403)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Secure task")

    def test_outsider_cannot_toggle_or_delete_task(self) -> None:
        self.client.force_login(self.outsider)
        toggle = self.client.post(
            reverse(
                "tasks:task-toggle-complete",
                kwargs={"pk": self.task.pk},
            )
        )
        delete = self.client.post(
            reverse("tasks:task-delete", kwargs={"pk": self.task.pk})
        )
        self.assertEqual(toggle.status_code, 403)
        self.assertEqual(delete.status_code, 403)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_outsider_cannot_manage_team_or_taxonomy(self) -> None:
        self.client.force_login(self.outsider)
        team_create = self.client.post(
            reverse("tasks:team-create"),
            data={"name": "Evil Team"},
        )
        tag_create = self.client.post(
            reverse("tasks:tag-create"),
            data={"name": "evil-tag"},
        )
        self.assertEqual(team_create.status_code, 403)
        self.assertEqual(tag_create.status_code, 403)

    def test_owner_can_update_task(self) -> None:
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("tasks:task-update", kwargs={"pk": self.task.pk}),
            data={
                "name": "Updated by owner",
                "description": "ok",
                "deadline": date.today().isoformat(),
                "priority": Task.Priority.HIGH,
                "task_type": self.task_type.pk,
                "project": self.project.pk,
                "assignees": [self.owner.pk],
                "is_completed": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated by owner")

    def test_staff_can_create_team(self) -> None:
        self.client.force_login(self.staff)
        response = self.client.post(
            reverse("tasks:team-create"),
            data={"name": "Ops", "members": [self.owner.pk]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Team.objects.filter(name="Ops").exists())
