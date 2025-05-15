from django.test import TestCase
from django.utils import timezone
from board.models import Position, Worker, TaskType, Task


class ModelTests(TestCase):
    def test_position_str(self):
        """Test __str__ method of Position model returns its name"""
        position = Position.objects.create(name="Developer")
        self.assertEqual(str(position), position.name)

    def test_worker_str(self):
        """Test __str__ method of Worker model returns 'First Last (username)'"""
        position = Position.objects.create(name="Manager")
        worker = Worker.objects.create_user(
            username="worker1",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            position=position
        )
        expected_str = f"{worker.first_name} {worker.last_name} ({worker.username})"
        self.assertEqual(str(worker), expected_str)

    def test_task_type_str(self):
        """Test __str__ method of TaskType model returns its name"""
        task_type = TaskType.objects.create(name="Bug")
        self.assertEqual(str(task_type), task_type.name)

    def test_task_str(self):
        """Test __str__ method of Task model returns its name"""
        task_type = TaskType.objects.create(name="Feature")
        position = Position.objects.create(name="Developer")
        worker = Worker.objects.create_user(
            username="worker2",
            password="testpass123",
            position=position
        )
        task = Task.objects.create(
            name="Fix bug",
            description="Fix the critical bug",
            deadline=timezone.now(),
            priority=Task.Priority.HIGH,
            task_type=task_type,
        )
        task.assignees.add(worker)
        self.assertEqual(str(task), task.name)

    def test_create_worker_with_position(self):
        """Test creating a Worker with a position and password hashing"""
        position = Position.objects.create(name="Tester")
        username = "worker3"
        password = "testpassword"
        worker = Worker.objects.create_user(
            username=username,
            password=password,
            position=position
        )
        self.assertEqual(worker.username, username)
        self.assertEqual(worker.position, position)
        self.assertTrue(worker.check_password(password))
