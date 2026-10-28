from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from tasks.models import Position, Project, Tag, Task, TaskType, Team

Worker = get_user_model()


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="dev.anna",
            password="pass12345",
            position=self.position,
        )
        self.team = Team.objects.create(name="Frontend Squad")
        self.team.members.add(self.worker)
        self.project = Project.objects.create(
            name="Vacancies Portal",
            team=self.team,
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.tag = Tag.objects.create(name="landing-page-layout")
        self.task = Task.objects.create(
            name="Fix Dashboard for Vacancies",
            description="Broken layout",
            deadline=date.today(),
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
            project=self.project,
            creator=self.worker,
        )
        self.task.assignees.add(self.worker)
        self.task.tags.add(self.tag)

    def test_str_representations(self) -> None:
        self.assertEqual(str(self.position), "Developer")
        self.assertIn("dev.anna", str(self.worker))
        self.assertEqual(str(self.team), "Frontend Squad")
        self.assertEqual(str(self.project), "Vacancies Portal")
        self.assertEqual(str(self.task_type), "Bug")
        self.assertEqual(str(self.tag), "landing-page-layout")
        self.assertEqual(str(self.task), "Fix Dashboard for Vacancies")

    def test_relationships(self) -> None:
        self.assertEqual(self.worker.position, self.position)
        self.assertIn(self.worker, self.team.members.all())
        self.assertEqual(self.project.team, self.team)
        self.assertIn(self.worker, self.task.assignees.all())
        self.assertIn(self.tag, self.task.tags.all())
        self.assertEqual(self.task.creator, self.worker)
        self.assertEqual(self.task.project, self.project)
