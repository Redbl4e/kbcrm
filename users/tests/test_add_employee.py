from copy import deepcopy

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()
CORRECT_FORM_DATA = {
    'last_name': 'test_ln',
    'first_name': 'test_fn',
    'patronymic': 'test_pt',
    'position': 'test_pos',
    'email': 'test@email.ru',
}

CORRECT_USERNAME = 'tt_test_ln_group'


class AddNewEmployeeTest(TestCase):

    def setUp(self) -> None:
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

    def tearDown(self) -> None:
        self.user.delete()
        self.staff_user.delete()

    def test_get_correct(self):
        staff_response = self.staff_client.get(reverse('users:add_employee'))
        self.assertEqual(200, staff_response.status_code)

    def test_get_no_permission(self):
        guest_response = self.guest_client.get(reverse('users:add_employee'))
        user_response = self.client.get(reverse('users:add_employee'))
        self.assertEqual(302, guest_response.status_code)
        self.assertEqual(302, user_response.status_code)

    def test_post_no_permission(self):
        guest_response = self.guest_client.post(reverse('users:add_employee'))
        user_response = self.client.post(reverse('users:add_employee'))
        self.assertEqual(302, guest_response.status_code)
        self.assertEqual(302, user_response.status_code)

    def test_post_correct(self):
        response = self.staff_client.post(
            reverse('users:add_employee'),
            CORRECT_FORM_DATA
        )
        response_username = response.context[0].dicts[3]['username']
        self.assertEqual(200, response.status_code)
        self.assertEqual(CORRECT_USERNAME, response_username)
        self.assertTrue(response.context[0].dicts[3]['password'])

    def test_post_miss_smth(self):
        for key in CORRECT_FORM_DATA:
            with self.subTest(key=key):
                data_with_one_miss = deepcopy(CORRECT_FORM_DATA)
                data_with_one_miss.pop(key)
                response = self.staff_client.post(
                    reverse('users:add_employee'),
                    data_with_one_miss
                )
                form_error_class = response.context['form'].errors[key].error_class
                self.assertEqual(form_error_class, 'errorlist')
                self.assertEqual(200, response.status_code)
