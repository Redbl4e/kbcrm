from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase


class AuthTest(TestCase):

    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user(
            username='test_username',
            password='test_password',
            email='test@email.ru',
            first_name='fn',
            last_name='ln',
            patronymic='pt',
            position='test_position'
        )
        self.user.save()

    def tearDown(self) -> None:
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test_username', password='test_password')
        self.assertTrue(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='test_username', password='wrong_password')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong_username', password='test_password')
        self.assertFalse(user is not None and user.is_authenticated)
