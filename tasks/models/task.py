from django.contrib.auth import get_user_model
from django.db import models

from tasks.models import Status

User = get_user_model()


class Task(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='название', db_index=True,
    )
    description = models.TextField(
        max_length=2000, verbose_name='описание',
        blank=True
    )
    guarantor = models.ForeignKey(
        to=User, on_delete=models.SET_NULL,
        null=True, verbose_name='поручитель', related_name='guarantor'
    )
    deadline = models.DateTimeField(
        verbose_name='крайний срок'
    )
    status = models.CharField(
        verbose_name='статус', max_length=41,
        choices=Status.choices, default=Status.CREATED,
        blank=True
    )
    file = models.ManyToManyField(
        through='TaskFileRelation',
        to='tasks.File',
        verbose_name='файлы', default=None,
        blank=True, related_name='file_tasks'
    )
    executor = models.ManyToManyField(
        to=User,
        verbose_name='исполнители', related_name='executor_tasks'
    )
    created_at = models.DateTimeField(
        verbose_name='создано', auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='изменено', auto_now=True
    )

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'

    def __str__(self):
        return f'{self.name[:10]} - {self.guarantor}'


class TaskFileRelation(models.Model):
    task = models.ForeignKey(
        'tasks.Task', on_delete=models.CASCADE,
        verbose_name='задача'
    )
    file = models.ForeignKey(
        'tasks.File', on_delete=models.CASCADE,
        verbose_name='файл'
    )

    class Meta:
        verbose_name = 'файлы и задачи'
        verbose_name_plural = 'файлы и задачи'

    def __str__(self):
        return f'{self.task.name} - {self.file.data.name}'
