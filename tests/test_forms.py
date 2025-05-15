from django.test import TestCase
from django.utils import timezone
from board.forms import WorkerCreationForm, WorkerUpdateForm, TaskCreateForm
from board.models import Worker, Position, TaskType


class WorkerCreationFormTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")

    def test_worker_creation_form_valid(self):
        """Test that the worker creation form is valid with correct data"""
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "position": self.position.id,
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(form.cleaned_data["first_name"], form_data["first_name"])
        self.assertEqual(form.cleaned_data["position"], self.position)


class WorkerUpdateFormTests(TestCase):
    def setUp(self):
        self.position1 = Position.objects.create(name="Developer")
        self.position2 = Position.objects.create(name="Manager")
        self.worker = Worker.objects.create_user(
            username="worker1",
            password="password123",
            first_name="Old",
            last_name="Name",
            position=self.position1
        )

    def test_worker_update_form_valid(self):
        """Test that the worker update form is valid with correct data"""
        form_data = {
            "username": "worker1",
            "first_name": "NewFirstName",
            "last_name": "NewLastName",
            "position": self.position2.id,
        }
        form = WorkerUpdateForm(data=form_data, instance=self.worker)
        self.assertTrue(form.is_valid())
        updated_worker = form.save(commit=False)
        self.assertEqual(updated_worker.first_name, form_data["first_name"])
        self.assertEqual(updated_worker.position.id, self.position2.id)

    def test_worker_update_form_username_already_exists(self):
        """Test validation error when updating username to one that already exists"""
        Worker.objects.create_user(username="existinguser", password="password123")

        form_data = {
            "username": "existinguser",  # duplicate username
            "first_name": "NewFirstName",
            "last_name": "NewLastName",
            "position": self.position1.id,
        }
        form = WorkerUpdateForm(data=form_data, instance=self.worker)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class TaskCreateFormTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker1 = Worker.objects.create_user(username="worker1", password="password123", position=self.position)
        self.worker2 = Worker.objects.create_user(username="worker2", password="password123", position=self.position)
        self.task_type = TaskType.objects.create(name="Bug")

    def test_task_create_form_valid(self):
        """Test that the task creation form is valid with correct data"""
        form_data = {
            "name": "Test task",
            "description": "Some description",
            "deadline": timezone.now().strftime("%Y-%m-%dT%H:%M"),  # datetime-local format
            "priority": "high",
            "task_type": self.task_type.id,
            "assignees": [self.worker1.id, self.worker2.id],
        }
        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        task = form.save(commit=False)
        self.assertEqual(task.name, form_data["name"])
        self.assertEqual(task.priority, form_data["priority"])
        self.assertEqual(task.task_type.id, self.task_type.id)
        task.save()
        form.save_m2m()
        self.assertEqual(list(task.assignees.all()), [self.worker1, self.worker2])

    def test_task_create_form_invalid_priority(self):
        """Test that the form is invalid with an incorrect priority value"""
        form_data = {
            "name": "Test task",
            "description": "Some description",
            "priority": "invalid_priority",
            "task_type": self.task_type.id,
        }
        form = TaskCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("priority", form.errors)
