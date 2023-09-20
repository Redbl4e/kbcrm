from django.urls import path, include

from .views import (
    LoginView, DivisionView, PasswordResetView, PasswordResetConfirmView, UpdateEmployeeView, CreateEmployeeView,
    password_change, delete_employee,
)

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('password_change/<int:pk>/', password_change, name='password_change'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('', include('django.contrib.auth.urls')),

    path('delete/<int:pk>/', delete_employee, name='delete_employee'),
    path('update/<int:pk>/', UpdateEmployeeView.as_view(), name='update_employee'),
    path('add_employee/', CreateEmployeeView.as_view(), name='create_employee'),
    path('division/', DivisionView.as_view(), name='division'),
]
