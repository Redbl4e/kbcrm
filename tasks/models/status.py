from django.db import models


class Status(models.TextChoices):
    EMPTY_LABEL = '', '----- Выберите статус -----'
    CREATED = 'CREATED', 'Поручено'
    PROGRESS = 'PROGRESS', 'В работе'
    VERIFICATION = 'VERIFICATION', 'На подтверждении'
    DONE = 'DONE', 'Выполнено'


class StatusChoice(models.Model):
    status_choices = [
        ('CREATED', 'Поручено'),
        ('PROGRESS', 'В работе'),
        ('VERIFICATION', 'На подтверждении'),
        ('DONE', 'Выполнено')
    ]
    status = models.CharField(max_length=255, choices=status_choices)
