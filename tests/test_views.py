from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from board.models import Task, Position, Worker, TaskType

class PublicViewsTests(TestCase):
    def test_redirect_if_not_logged_in(self):
        """Test that login is required for all protected views"""
        urls = [
            reverse("board:task-list"),
            reverse("board:worker-list"),
        ]
        position = Position.objects.create(name="Tester")
        worker = get_user_model().objects.create_user(username="worker1", password="pass123", position=position)
        task_type = TaskType.objects.create(name="Bug")
        task = Task.objects.create(name="Test Task", description="Desc", task_type=task_type)
        task.assignees.add(worker)

        urls += [
            reverse("board:task-detail", kwargs={"pk": task.pk}),
            reverse("board:task-update", kwargs={"pk": task.pk}),
            reverse("board:task-delete", kwargs={"pk": task.pk}),
            reverse("board:task-create"),
            reverse("board:worker-create"),
            reverse("board:worker-update", kwargs={"pk": worker.pk}),
            reverse("board:worker-delete", kwargs={"pk": worker.pk}),
            reverse("board:worker-profile-detail", kwargs={"pk": worker.pk}),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)
            self.assertIn(response.status_code, [302, 301])  # redirect to login

class PrivateViewsTests(TestCase):
    def setUp(self):
        """Create a user and login"""
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.force_login(self.user)

        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="worker1",
            password="workerpass",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Feature")
        self.task = Task.objects.create(
            name="Task 1",
            description="Task description",
            task_type=self.task_type
        )
        self.task.assignees.add(self.worker)

    def test_task_list_view(self):
        """Test task list view returns correct template and context"""
        url = reverse("board:task-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "board/tasks_list.html")
        self.assertIn("tasks", response.context)
        self.assertIn(self.task, response.context["tasks"])

    def test_task_detail_view(self):
        """Test task detail view returns 200 and correct task"""
        url = reverse("board:task-detail", kwargs={"pk": self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["task"], self.task)

    def test_task_create_view(self):
        """Test creating a new task via form"""
        url = reverse("board:task-create")
        data = {
            "name": "New Task",
            "description": "Some description",
            "priority": Task.Priority.MEDIUM,
            "task_type": self.task_type.pk,
            "assignees": [self.worker.pk],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # redirect after success
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_worker_list_view(self):
        """Test worker list view returns correct template and context"""
        url = reverse("board:worker-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "board/workers_list.html")
        self.assertIn("workers", response.context)
        self.assertIn(self.worker, response.context["workers"])

    def test_worker_create_view(self):
        """Test creating a new worker"""
        url = reverse("board:worker-create")
        data = {
            "username": "newworker",
            "password1": "newpass123",
            "password2": "newpass123",
            "first_name": "First",
            "last_name": "Last",
            "position": self.position.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="newworker").exists())

    def test_worker_update_view(self):
        """Test updating a worker"""
        url = reverse("board:worker-update", kwargs={"pk": self.worker.pk})
        data = {
            "username": self.worker.username,
            "first_name": "UpdatedFirst",
            "last_name": "UpdatedLast",
            "position": self.position.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.first_name, "UpdatedFirst")
        self.assertEqual(self.worker.last_name, "UpdatedLast")

    def test_worker_profile_detail_view(self):
        """Test worker profile detail page"""
        url = reverse("board:worker-profile-detail", kwargs={"pk": self.worker.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["worker"], self.worker)
