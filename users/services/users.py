from django.contrib.auth.models import Group

from users.forms import UserCreationForm
from users.services import generate_auth_data


def create_new_user_and_return_context(form: UserCreationForm, group: Group) -> dict:
    new_user = form.save(commit=False)
    auth_data = generate_auth_data(new_user, group.name)
    new_user.username = auth_data.username
    new_user.set_password(auth_data.password)
    new_user.save()
    group.user_set.add(new_user.id)
    context = {
        'username': auth_data.username,
        'password': auth_data.password
    }
    return context
