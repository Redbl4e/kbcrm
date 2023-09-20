from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status

from users.tests.base_setup import BaseTest

User = get_user_model()


class EmployeeTestCase(BaseTest):

    def setUp(self) -> None:
        super().setUp()

    def test_get_correct(self):
        client_response = self.client.get(reverse('users:division'))
        staff_response = self.staff_client.get(reverse('users:division'))
        self.assertEqual(client_response.status_code, status.HTTP_200_OK)
        self.assertEqual(staff_response.status_code, status.HTTP_200_OK)

    def test_get_no_permission(self):
        guest_response = self.guest_client.get(reverse('users:division'))
        self.assertEqual(guest_response.status_code, status.HTTP_302_FOUND)

    def test_change_password_correct(self):
        old_password = self.user.password
        staff_response = self.staff_client.get(reverse('users:password_change', args=[self.user.pk]))
        new_password_in_context = staff_response.context[0].dicts[3]['password']
        new_password = make_password(new_password_in_context)
        self.assertEqual(staff_response.status_code, status.HTTP_200_OK)
        self.assertTrue(new_password_in_context)
        self.assertNotEqual(old_password, new_password)

    def test_change_password_no_permission(self):
        old_password = self.user.password
        guest_response = self.guest_client.get(reverse('users:password_change', args=[self.user.pk]))
        response = self.client.get(reverse('users:password_change', args=[self.user.pk]))
        new_password = self.user.password
        self.assertEqual(guest_response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(old_password, new_password)

    def test_delete_employee_done(self):
        staff_response = self.staff_client.get(reverse('users:delete_employee', args=[self.user.pk]))
        self.assertEqual(staff_response.status_code, status.HTTP_302_FOUND)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get()

    def test_delete_no_permission(self):
        guest_response = self.guest_client.get(reverse('users:delete_employee', args=[self.user.pk]))
        self.assertEqual(guest_response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(User.objects.get())
        response = self.client.get(reverse('users:delete_employee', args=[self.user.pk]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(User.objects.get())
