from typing import Any
from django.contrib.auth.models import BaseUserManager
from django.db import transaction

from .utils import send_activation_code


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff=False, is_superuser=False, is_active=False, **extra_fields: Any):
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            full_name=extra_fields.get('full_name'),
        )

        user.set_password(password)
        user.save()

        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(
            email=email,
            password=password,
            is_staff=False,
            is_superuser=False,
            is_active=True,
            full_name=extra_fields.get('full_name'),
        )

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            full_name=extra_fields.get('full_name'),
        )

    def create(self, email, password, **extra_fields):
        with transaction.atomic():
            user = self.model(
                email=email,
                is_staff=False,
                is_superuser=False,
                is_active=False,
                full_name=extra_fields.get('full_name'),
            )

            user.set_password(password)
            user.save()

            try:
                send_activation_code(
                    user=user
                )
            except Exception as e:
                raise e

            return user
