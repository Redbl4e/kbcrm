from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import Client, TestCase

User = get_user_model()


class BaseTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create()
        self.group.name = 'group'
        self.group.save()

        self.guest_client = Client()

        self.user = User.objects.create_user(username='username', password='password')
        self.user.save()
        self.client = Client()
        self.client.force_login(self.user)

        self.staff_user = User.objects.create_user(username='staff_username', password='staff_password')
        self.staff_user.is_staff = True
        self.staff_user.save()
        self.staff_client = Client()
        self.staff_client.force_login(self.staff_user)

        self.group.user_set.add(self.user.id)
        self.group.user_set.add(self.staff_user.id)
