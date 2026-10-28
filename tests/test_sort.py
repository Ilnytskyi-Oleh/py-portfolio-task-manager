from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from tasks.models import Position, Project, Task, TaskType, Team

Worker = get_user_model()


class TaskSortTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="sorter",
            password="pass12345",
            position=position,
        )
        team = Team.objects.create(name="Sort Team")
        team.members.add(self.worker)
        project = Project.objects.create(name="Sort Project", team=team)
        task_type = TaskType.objects.create(name="Bug")
        today = date.today()
        Task.objects.create(
            name="Alpha task",
            deadline=today + timedelta(days=5),
            priority=Task.Priority.LOW,
            task_type=task_type,
            project=project,
            creator=self.worker,
            is_completed=False,
        )
        Task.objects.create(
            name="Bravo task",
            deadline=today + timedelta(days=1),
            priority=Task.Priority.URGENT,
            task_type=task_type,
            project=project,
            creator=self.worker,
            is_completed=True,
        )
        self.client.force_login(self.worker)

    def test_sort_by_name_asc(self) -> None:
        response = self.client.get(
            reverse("tasks:task-list"),
            {"sort": "name", "dir": "asc"},
        )
        self.assertEqual(response.status_code, 200)
        names = [task.name for task in response.context["task_list"]]
        self.assertEqual(names, sorted(names))

    def test_sort_by_priority_puts_urgent_first(self) -> None:
        response = self.client.get(
            reverse("tasks:task-list"),
            {"sort": "priority", "dir": "asc"},
        )
        self.assertEqual(response.status_code, 200)
        tasks = list(response.context["task_list"])
        self.assertEqual(tasks[0].priority, Task.Priority.URGENT)
        self.assertEqual(tasks[-1].priority, Task.Priority.LOW)

    def test_sort_by_status(self) -> None:
        response = self.client.get(
            reverse("tasks:task-list"),
            {"sort": "status", "dir": "asc"},
        )
        self.assertEqual(response.status_code, 200)
        flags = [task.is_completed for task in response.context["task_list"]]
        self.assertEqual(flags, sorted(flags))
