import random
from builtins import enumerate
from dataclasses import dataclass

from django.conf import settings

User = settings.AUTH_USER_MODEL

SYMBOLS = '23456789abcdefghigkmnpqrstuvyxwzABCDEFGHIGKLMNPQRSTUVYXWZ'


@dataclass
class AuthData:
    username: str
    password: str


def generate_auth_data(user: User, group_name: str) -> AuthData:
    fio_group = (
        user.first_name,
        user.patronymic,
        user.last_name,
        group_name
    )
    username, password = _generate_tuple_of_raw_login_password(fio_group)
    translated_login = _translate_username_to_rus(username)
    translated_login = translated_login.lower().replace(' ', '_')
    auth_data = AuthData(
        translated_login, password
    )
    # if ab[0] == abc[0]:
    #     login = f'{abc[0]}_{str(randint(10, 100))}'
    return auth_data


def generate_password(length: int = 10) -> str:
    password = ''
    for _ in range(0, length):
        password += random.choice(SYMBOLS)
    return password


def _generate_tuple_of_raw_login_password(fio_group: tuple[str]) -> tuple[str, str]:
    username = ''
    password = generate_password()

    for idx, _ in enumerate(fio_group):
        if idx == 0:
            username += fio_group[idx][0]
        elif idx == 1:
            username += f'{fio_group[idx][0]}_'
        elif idx == 2:
            username += f'{fio_group[idx]}_'
        else:
            username += fio_group[idx]
    return username, password


def _translate_username_to_rus(username: str):
    dic = {'ь': '', 'ъ': '', 'а': 'a', 'б': 'b', 'в': 'v',
           'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
           'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l',
           'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
           'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
           'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ы': 'yi',
           'э': 'e', 'ю': 'yu', 'я': 'ya'}

    translation_login = ''
    for i in username:
        translation_login += dic.get(i.lower(), i.lower()).upper() if i.isupper() else dic.get(i, i)
    return translation_login
