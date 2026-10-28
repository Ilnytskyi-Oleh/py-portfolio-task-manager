from datetime import date

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from tasks.models import Position, Project, Tag, Task, TaskType, Team

Worker = get_user_model()


class ViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="dev.anna",
            password="pass12345",
            first_name="Anna",
            last_name="Dev",
            position=self.position,
        )
        self.team = Team.objects.create(name="Frontend Squad")
        self.team.members.add(self.worker)
        self.project = Project.objects.create(
            name="Vacancies Portal",
            team=self.team,
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.tag = Tag.objects.create(name="python-refactoring")
        self.task = Task.objects.create(
            name="Fix Dashboard",
            deadline=date.today(),
            task_type=self.task_type,
            project=self.project,
            creator=self.worker,
            is_completed=False,
        )
        self.task.assignees.add(self.worker)
        self.task.tags.add(self.tag)
        self.done_task = Task.objects.create(
            name="Done task",
            task_type=self.task_type,
            project=self.project,
            creator=self.worker,
            is_completed=True,
        )
        self.done_task.assignees.add(self.worker)

    def test_login_required(self) -> None:
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_index_authenticated(self) -> None:
        self.client.force_login(self.worker)
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")
        self.assertEqual(response.context["my_open_tasks"], 1)
        self.assertEqual(response.context["my_done_tasks"], 1)

    def test_worker_detail_splits_tasks(self) -> None:
        self.client.force_login(self.worker)
        response = self.client.get(
            reverse("tasks:worker-detail", kwargs={"pk": self.worker.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.task, response.context["incomplete_tasks"])
        self.assertIn(self.done_task, response.context["completed_tasks"])
        self.assertNotIn(self.task, response.context["completed_tasks"])

    def test_create_task(self) -> None:
        self.client.force_login(self.worker)
        response = self.client.post(
            reverse("tasks:task-create"),
            data={
                "name": "New feature task",
                "description": "Add Google sign-in",
                "deadline": date.today().isoformat(),
                "priority": Task.Priority.HIGH,
                "task_type": self.task_type.pk,
                "project": self.project.pk,
                "assignees": [self.worker.pk],
                "tags": [self.tag.pk],
                "tag_names": "auth, api",
                "is_completed": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(name="New feature task")
        self.assertEqual(task.creator, self.worker)
        self.assertIn(self.worker, task.assignees.all())
        self.assertTrue(task.tags.filter(name="auth").exists())
        self.assertTrue(task.tags.filter(name="api").exists())

    def test_toggle_complete(self) -> None:
        self.client.force_login(self.worker)
        response = self.client.post(
            reverse(
                "tasks:task-toggle-complete",
                kwargs={"pk": self.task.pk},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)

    def test_project_and_team_pages(self) -> None:
        self.client.force_login(self.worker)
        project_resp = self.client.get(
            reverse("tasks:project-detail", kwargs={"pk": self.project.pk})
        )
        team_resp = self.client.get(
            reverse("tasks:team-detail", kwargs={"pk": self.team.pk})
        )
        self.assertEqual(project_resp.status_code, 200)
        self.assertEqual(team_resp.status_code, 200)
        self.assertContains(project_resp, self.project.name)
        self.assertContains(team_resp, self.team.name)
        self.assertContains(team_resp, self.worker.username)

    def test_task_list_filter_by_tag(self) -> None:
        self.client.force_login(self.worker)
        response = self.client.get(
            reverse("tasks:task-list"),
            {"tag": self.tag.pk},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)
        self.assertNotContains(response, self.done_task.name)
