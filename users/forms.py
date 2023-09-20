from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import (
    AuthenticationForm as DjangoAuthenticationForm,
    UsernameField,
    SetPasswordForm as DjangoSetPasswordForm
)
from django.forms import TextInput, ModelForm, EmailInput

User = get_user_model()


class AuthenticationForm(DjangoAuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={
            'type': 'text',
            'name': 'username',
            'class': 'form-control text-center text-lowercase',
            'placeholder': 'Имя пользователя',
        }
    ))
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'name': 'password',
                'id': 'password',
                'class': 'form-control text-center text-lowercase',
                'placeholder': 'пароль',
                'autocomplete': 'current-password',
            }),
    )


class UserCreationForm(ModelForm):
    email = forms.EmailField(
        label='Email адрес',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'name': 'email-add',
            'id': 'email-add',
            'class': 'bg-gray-200 border border-gray-300 text-gray-900 text-sm rounded-r-lg w-full p-2.5',
            'placeholder': 'example@email.ru'
        }
        )
    )
    is_staff = forms.BooleanField(
        label='Начальник',
        help_text='',
        required=False
    )

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic',
                  'is_staff', 'position', 'email')
        widgets = {
            'first_name': TextInput(attrs={
                'type': 'text',
                'name': 'first-name-add',
                'id': 'first-name-add',
                'placeholder': '',
                'class': 'bg-gray-200 border border-gray-300 text-gray-900 text-sm rounded-r-lg w-full p-2.5'
            }),
            'last_name': TextInput(attrs={
                'type': 'text',
                'name': 'last-name-add',
                'id': 'last-name-add',
                'placeholder': '',
                'class': 'bg-gray-200 border border-gray-300 text-gray-900 text-sm rounded-r-lg w-full p-2.5'
            }),

            'patronymic': TextInput(attrs={
                'type': 'text',
                'name': 'patronymic-add',
                'id': 'patronymic-add',
                'placeholder': '',
                'class': 'bg-gray-200 border border-gray-300 text-gray-900 text-sm rounded-r-lg w-full p-2.5'
            }),
            'position': TextInput(attrs={
                'type': 'text',
                'name': 'position-add',
                'id': 'position-add',
                'placeholder': '',
                'class': 'bg-gray-200 border border-gray-300 text-gray-900 text-sm rounded-r-lg w-full p-2.5'
            }),
        }


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic', 'is_staff', 'position', 'email')
        widgets = {
            'last_name': TextInput(attrs={
                'class': 'pl-4 py-2.5 rounded-none rounded-r-lg bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }),
            'first_name': TextInput(attrs={
                'class': 'pl-4 py-2.5 rounded-none rounded-r-lg bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }),
            'patronymic': TextInput(attrs={
                'class': 'pl-4 py-2.5 rounded-none rounded-r-lg bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }),
            'position': TextInput(attrs={
                'class': 'pl-4 py-2.5 rounded-none rounded-r-lg bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
            }),
            'email': EmailInput(attrs={
                'class': 'pl-4 py-2.5 rounded-none rounded-r-lg bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }),
        }


class SetPasswordForm(DjangoSetPasswordForm):
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'mx-auto text-center text-gray-900 sm:text-sm block w-[75%] p-2.5'
            }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Подтвердите новый пароль',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'mx-auto text-center text-gray-900 sm:text-sm block w-[75%] p-2.5'
            }),
    )
