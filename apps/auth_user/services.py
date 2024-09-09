from django.core.exceptions import ValidationError

from .exceptions import UserNotFound
from .models import User
from .utils import check_activation_code, check_password_reset_code, send_password_reset_code, \
    send_password_change_code, check_password_change_code


class UserActivateService:
    def __init__(self, email: str, activation_code: int):
        self.email = email
        self.activation_code = activation_code

    def activate_user(self) -> User:
        try:
            user = User.objects.get(email=self.email)
        except User.DoesNotExist:
            raise UserNotFound

        if not check_activation_code(user=user, code=self.activation_code):
            raise ValidationError('Invalid activation code')

        user.is_active = True
        user.save()

        return user


class UserPasswordResetService:
    def __init__(self, activation_code: int, email: str):
        self.activation_code = activation_code
        self.email = email

    def reset_password(self):
        try:
            user = User.objects.get(email=self.email)
        except User.DoesNotExist:
            raise UserNotFound

        send_password_reset_code(user)


class UserPasswordResetConfirmService:
    def __init__(self, email: str, activation_code: int, password_confirm: str):
        self.email = email
        self.activation_code = activation_code
        self.password_confirm = password_confirm

    def reset_password_confirm(self) -> User:
        try:
            user = User.objects.get(email=self.email)
        except User.DoesNotExist:
            raise UserNotFound

        if not check_password_reset_code(user=user, code=self.activation_code):
            raise ValidationError('Invalid password reset code')

        user.set_password(self.password_confirm)
        user.save()
        return user


class UserForgotPasswordService:
    def __init__(self, email: str):
        self.email = email

    def forgot_password(self):
        try:
            user = User.objects.get(email=self.email)
        except User.DoesNotExist:
            raise UserNotFound

        send_password_change_code(user)
        return user


class UserChangePasswordService:
    def __init__(self, email: str, activation_code: int, new_password_confirm: str):
        self.email = email
        self.activation_code = activation_code
        self.new_password_confirm = new_password_confirm

    def change_password(self) -> User:
        try:
            user = User.objects.get(email=self.email)
        except User.DoesNotExist:
            raise UserNotFound

        if not check_password_change_code(user=user, code=self.activation_code):
            raise ValidationError('Invalid password change code')

        user.set_password(self.new_password_confirm)
        user.save()
        return user

