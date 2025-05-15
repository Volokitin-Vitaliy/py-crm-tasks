from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from board.models import Position


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)

        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="testworker",
            position=self.position
        )

    def test_worker_change_page_displays_position(self):
        """Check that the user edit page shows the position"""
        url = reverse("admin:board_worker_change", args=[self.worker.id])
        res = self.client.get(url)
        self.assertContains(res, self.position.name)

    def test_worker_list_page_displays_position(self):
        """We check that the position is shown in the list of admin users"""
        url = reverse("admin:board_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.position.name)