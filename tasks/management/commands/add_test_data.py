import random
from datetime import datetime, timedelta

import pytz
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from tasks.models import Task, Status
from users.services import generate_auth_data

User = get_user_model()


class Command(BaseCommand):
    help = 'Populates the database with random generated data.'

    def add_arguments(self, parser):
        parser.add_argument('--amount', type=int, help='The number of purchases that should be created.')

    def handle(self, *args, **options):
        first_names = ['Кирилл', 'Сергей', 'Павел', 'Даниил', 'Богдан', 'Вячеслав', 'Дмитрий', 'Илья']
        last_names = ['Редько', 'Лавров', 'Прокофьев', 'Белоус', 'Иванов', 'Ларичев', 'Решетнёв', 'Никулин']
        patronymics = ['Сергеевич', 'Павлович', 'Дмитриевич', 'Алексеевич', 'Петрович', 'Александрович', 'Ильич',
                       'Артёмович']
        positions = ['Преподаватель', 'Старший преподаватель', 'Методист', 'Доцент', 'Профессор']
        group_ids = [1, 2, 3, 4, 5]

        amount = options['amount'] if options['amount'] else 2500
        # for i in range(0, 150):
        #     # Create users
        #     user = User()
        #     user.first_name = random.choice(first_names)
        #     user.last_name = random.choice(last_names)
        #     user.patronymic = random.choice(patronymics)
        #     user.position = random.choice(positions)
        #     user.is_staff = random.choice([True, False])
        #     group = Group.objects.get(pk=random.choice(group_ids))
        #     auth_data = generate_auth_data(user, group.name)
        #     user.username = auth_data.username
        #     user.set_password(auth_data.password)
        #     try:
        #         user.save()
        #     except IntegrityError:
        #         continue
        #     group.user_set.add(user.id)

        task_names = ['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 5']
        statuses = ['CREATED', 'PROGRESS', 'VERIFICATION', 'DONE']
        # Create tasks
        for i in range(0, amount):
            task = Task()
            users = User.objects.all()
            task.name = random.choice(task_names)
            task.deadline = pytz.utc.localize(datetime.now() - timedelta(days=random.randint(0, 5)))
            task.status = 'DONE'
            task.guarantor = random.choice(users)
            task.save()
            for j in range(random.randint(1, 5)):
                task.executor.add(random.choice(users))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database.'))
