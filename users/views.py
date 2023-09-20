from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    PasswordResetView as DjangoPasswordResetView,
    PasswordResetConfirmView as DjangoPasswordResetConfirmView
)
from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, UpdateView

from .forms import AuthenticationForm, UserCreationForm, SetPasswordForm, UserUpdateForm
from .services.users import create_new_user_and_return_context

from config.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

User = get_user_model()


class DivisionView(ListView):
    model = User
    template_name = 'users/division_list.html'
    context_object_name = 'employees'

    @method_decorator(login_required(login_url='users:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, **kwargs):
        group_id = self.request.user.groups.get().id
        employees = User.objects.filter(groups__id=group_id).order_by('-is_staff').order_by('pk')
        form = UserCreationForm()
        context = {
            'employees': employees,
            'form': form
        }
        return render(request, self.template_name, context)


class CreateEmployeeView(View):
    def post(self, request):
        form = UserCreationForm(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            try:
                group = request.user.groups.get()
            except ObjectDoesNotExist:
                return redirect('users:division')
            context = create_new_user_and_return_context(form, group)
            email = form.cleaned_data.get('email')
            password = context.get('password')
            send_mail(subject='СRM_SWIPE_PASSWORD', message=f'Ваш пароль, сохраните его: {password}',
                      recipient_list=[email], from_email=EMAIL_HOST_USER)
            return render(request, 'users/add_employee_done.html', context)
        return render(request, 'users/division_list.html', context)


class UpdateEmployeeView(UpdateView):
    model = User
    template_name = 'users/update_employee.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:division')

    @method_decorator(staff_member_required(login_url='users:login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@staff_member_required(login_url='users:login')
def delete_employee(request: WSGIRequest, pk: int):
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect('users:division')


@staff_member_required(login_url='users:login')
def password_change(request: WSGIRequest, pk: int):
    # TODO сделать отправку нового пароля пользователю
    user = User.objects.get(pk=pk)
    new_password = user.change_password()
    context = {
        'password': new_password
    }
    return render(request, 'registration/password_change_complete.html', context)


class LoginView(DjangoLoginView):
    form_class = AuthenticationForm


class PasswordResetView(DjangoPasswordResetView):
    success_url = reverse_lazy('users:password_reset_done')


class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = reverse_lazy("users:password_reset_complete")
