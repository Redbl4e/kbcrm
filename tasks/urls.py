from django.urls import path

from .views import *

app_name = 'tasks'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('task/<int:pk>', TaskUpdateView.as_view(), name='update_task'),
    path('efficiency/<str:group_name>', efficiency_view, name='efficiency'),

    path('api/user_tasks/<int:days>/', get_user_tasks, name='user_tasks'),
    path('api/division_tasks/<int:days>/', get_all_division_tasks, name='division_tasks'),
    path('api/task_list/', TaskApiView.as_view(), name='task_api')
]
