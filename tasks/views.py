from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.models import Group, AbstractUser
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AddTaskForm, TaskFileForm, EditTaskForm
from .models import File, Task, Status
from .models.task import TaskFileRelation
from .serializers import TaskSerializer
from .services.charts import get_grouped_tasks_by_executor_in_json, get_all_division_tasks_in_json

User: AbstractUser = get_user_model()


class HomeView(View):

    def __init__(self, **kwargs):
        super().__init__()
        self.context = {}
        self.user = None
        self.group_name = None

    def setup(self, request, *args, **kwargs):
        super().setup(self, request, args, kwargs)
        try:
            self.group_name = request.user.groups.get().name
        except Group.DoesNotExist:
            self.group_name = None
        self.user = get_user(request)
        if self.user.is_staff:
            tasks = Task.objects.filter(Q(executor=self.user.id) | Q(guarantor=self.user.id)).filter(~Q(status='DONE')) \
                .select_related('guarantor').prefetch_related('executor', 'file').order_by('-created_at')
        else:
            tasks = Task.objects.filter(executor=self.user.id).filter(~Q(status='DONE')) \
                .select_related('guarantor').prefetch_related('executor', 'file').order_by('-created_at')
        task_form = AddTaskForm(self.group_name, initial={'status': Status.CREATED})
        file_form = TaskFileForm()

        self.context = {
            'tasks': tasks,
            'task_form': task_form,
            'file_form': file_form
        }

    def get(self, request, *args, **kwargs):
        if self.group_name is None:
            return redirect('users:login')
        return render(request, 'home.html', self.context)

    def post(self, request, *args, **kwargs):
        task_form = AddTaskForm(self.group_name, request.POST)
        file_form = TaskFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('data')
        if task_form.is_valid() and file_form.is_valid():
            self.save_task_form_with_files(request, task_form, files)
        return render(request, 'home.html', self.context)

    @staticmethod
    def save_task_form_with_files(request: WSGIRequest, task_form: AddTaskForm,
                                  files: list):
        executors = task_form.cleaned_data['executor']
        task = task_form.save(commit=False)
        task.guarantor = request.user
        task.save()
        task.executor.add(*executors)
        for file in files:
            file = File.objects.create(data=file)
            TaskFileRelation.objects.create(task=task, file=file)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = EditTaskForm
    template_name = 'tasks/update_task.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks:home')

    def get_object(self, queryset=None):
        task_pk = self.kwargs.get('pk')
        task = Task.objects.filter(pk=task_pk).select_related('guarantor').prefetch_related('executor', 'file').first()
        return task


@staff_member_required(login_url='users:login')
def efficiency_view(request, group_name: str):
    context = {
        'group_name': group_name
    }
    return render(request, 'tasks/efficiency.html', context)


@staff_member_required(login_url='users:login')
def get_user_tasks(request: WSGIRequest, days: int):
    user_group_id = request.user.groups.get().id
    json_response = get_grouped_tasks_by_executor_in_json(user_group_id, days)
    return json_response


@staff_member_required(login_url='users:login')
def get_all_division_tasks(request: WSGIRequest, days: int):
    user_group_id = request.user.groups.get().id
    json_response = get_all_division_tasks_in_json(user_group_id, days)
    return json_response


class TaskApiView(APIView):
    def __init__(self, **kwargs):
        super().__init__()
        self.user = None
        self.group_name = None
        self.context = {}

    def setup(self, request, *args, **kwargs):
        super().setup(self, request, args, kwargs)
        self.user = get_user(request)
        try:
            self.group_name = self.user.groups.get().name
        except Group.DoesNotExist:
            self.group_name = None
        task_json = Task.objects.filter(executor=self.user.id).filter(~Q(status='DONE')) \
            .select_related('guarantor').prefetch_related('executor', 'file').order_by('-created_at')
        serialized_tasks = TaskSerializer(task_json, many=True).data
        self.context = serialized_tasks

    def get(self, request):
        if self.group_name is None:
            return redirect('users:login')
        return Response(self.context)
