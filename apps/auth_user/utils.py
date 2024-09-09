from random import randint
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import transaction

from .exceptions import UserEmailSettingsFailed
from ..config import settings


def _generate_activation_code():
    return randint(1000, 9999)


def _send_code(user, cache_key: str, text: str, code: int):
    with transaction.atomic():
        cache.set(f'{cache_key}_{user.id}', code, timeout=300)  # 5 minutes

        try:
            send_mail(
                subject='Code confirmation',
                message=text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
        except Exception as e:
            raise UserEmailSettingsFailed


def _check_code(user, cache_key: str, code: int):
    return cache.get(f'{cache_key}_{user.id}') == code


def send_activation_code(user):
    code = _generate_activation_code()
    print(code)
    text = f'Your activation code: {code}'

    _send_code(user, 'activation_code', text, code)


def send_password_reset_code(user):
    code = _generate_activation_code()
    text = f'Your password reset code: {code}'

    _send_code(user, 'password_reset_code', text, code)


def send_password_change_code(user):
    code = _generate_activation_code()
    text = f'Your password change code: {code}'

    _send_code(user, 'password_change_code', text, code)


def check_activation_code(user, code: int):
    return _check_code(user, 'activation_code', code)


def check_password_reset_code(user, code: int):
    return _check_code(user, 'password_reset_code', code)


def check_password_change_code(user, code: int):
    return _check_code(user, 'password_change_code', code)
