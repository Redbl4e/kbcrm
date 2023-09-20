from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()


class TaskViewTest(TestCase):
    def setUp(self) -> None:
        self.group = Group.objects.create()
        self.group.name = 'group'
        self.group.save()
        self.user = User.objects.create_user(username='username', password='password')
        self.user.save()
        self.client = Client()
        self.client.force_login(self.user)
        self.group.user_set.add(self.group.id)

    def test_view_tasklist(self):
        response = self.client.get(reverse("tasks:home"))
        response_context_get = response.context.get('tasks')
        self.assertFalse(response_context_get)
