from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count, Q, F
from django.db.models import QuerySet
from django.http import JsonResponse
from django.utils import timezone

from tasks.models import Task

User = get_user_model()


def get_grouped_tasks_by_executor_in_json(user_group_id: int, days: int) -> JsonResponse:
    ranged_user_tasks = _get_user_tasks_by_range(user_group_id, days)
    grouped_tasks = _get_grouped_tasks_by_executor(ranged_user_tasks)
    tasks_dict = {}
    for task_group in grouped_tasks:
        fio = f'''{task_group['last_name']} {task_group['first_name'][:1]}.{task_group['patronymic'][:1]}.'''
        tasks_dict[fio] = [task_group['total_tasks'], task_group['completed_tasks']]
    json_response = JsonResponse({
        'title': '',
        'data': {
            'labels': list(tasks_dict.keys()),
            'datasets': [
                {
                    'label': 'Выполнено',
                    'backgroundColor': '#EEE8DA',
                    'data': [value[1] for value in tasks_dict.values()]
                },
                {
                    'label': 'Всего',
                    'backgroundColor': '#30627A',
                    'data': [value[0] for value in tasks_dict.values()]
                }
            ]
        },
    })
    return json_response


def get_all_division_tasks_in_json(user_group_id: int, days: int) -> JsonResponse:
    user_tasks = _get_user_tasks_by_range(user_group_id, days)
    grouped_tasks = user_tasks.aggregate(total_tasks=Count('id'), completed_tasks=Count('id', filter=Q(status='DONE')))
    tasks_list = [grouped_tasks['total_tasks'] - grouped_tasks['completed_tasks'], grouped_tasks['completed_tasks']]
    json_response = JsonResponse({
        'title': '',
        'data': {
            'labels': ['Не выполнено', 'Выполнено'],
            'datasets': [
                {
                    'label': 'Общая статистика',
                    'backgroundColor': ['#EEE8DA', '#30627A'],
                    'data': tasks_list
                },
            ]
        }
    })
    return json_response


def _get_grouped_tasks_by_executor(ranged_user_tasks: QuerySet) -> QuerySet:
    grouped_tasks = ranged_user_tasks.annotate(total_tasks=Count('id')).values('total_tasks') \
        .annotate(completed_tasks=Count('id', filter=Q(status='DONE'))) \
        .annotate(last_name=F('executor__last_name')) \
        .annotate(first_name=F('executor__first_name')) \
        .annotate(patronymic=F('executor__patronymic')) \
        .values('total_tasks', 'completed_tasks', 'last_name', 'first_name', 'patronymic')

    return grouped_tasks


def _get_user_tasks_by_range(user_group_id: int, days: int) -> QuerySet:
    users_ids = User.objects.filter(groups__id=user_group_id).values_list('id')
    user_tasks = Task.objects.filter(executor__in=users_ids).filter(
        deadline__range=(timezone.now() - timedelta(days), timezone.now()))
    return user_tasks
