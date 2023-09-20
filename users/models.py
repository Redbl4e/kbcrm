from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.services import generate_password


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name='имя пользователя', max_length=150, unique=True,
        validators=[username_validator],
        error_messages={
            "unique": "Пользователь с таким именем пользователя уже существует"
        }
    )
    first_name = models.CharField('имя', max_length=150)
    last_name = models.CharField('фамилия', max_length=150)
    email = models.EmailField(verbose_name='email адрес')
    patronymic = models.CharField(max_length=255, verbose_name='отчество')
    position = models.CharField(max_length=255, verbose_name='должность')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def change_password(self):
        new_password = generate_password()
        self.set_password(new_password)
        self.save()
        return new_password
