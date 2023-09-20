from django import forms
from django.contrib.auth import get_user_model

from users.models import User
from .models import Task, File

User: User = get_user_model()


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('status', )
        widgets = {
            'status': forms.Select(attrs={
                'class': 'rounded-none rounded-r-lg bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            })
        }


class AddTaskForm(forms.ModelForm):
    name = forms.CharField(
        label='Название задачи',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'block rounded-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder': ' '
            }
        )
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Описание задачи'
            }
        )
    )
    executor = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            }
        ),
        queryset=None
    )
    deadline = forms.DateTimeField(
        label='Крайний срок',
        widget=forms.DateTimeInput(
            format='%Y.%m.%d %H:%M',
            attrs={
                'type': 'datetime-local',
                'class': 'block rounded-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            }
        )
    )

    class Meta:
        model = Task
        fields = (
            'name', 'description', 'deadline',
            'status', 'executor'
        )

    def __init__(self, group_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].queryset = User.objects.filter(groups__name=group_name)


class TaskFileForm(forms.ModelForm):
    data = forms.FileField(
        required=False,
        label='',
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True,
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-white focus:outline-none'
            }
        )
    )

    class Meta:
        model = File
        fields = ('data',)
