from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ...config import settings
from .. import exceptions
from ..models import User


BASE_PASSWORD = settings.BASE_PASSWORD


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email, password = attrs['email'], attrs['password']

        user = User.objects.filter(email=email).first()

        if not user:
            raise exceptions.UserNotFound

        if not user.is_active:
            raise exceptions.UserNotActive

        if user.check_password(BASE_PASSWORD):
            raise exceptions.UserPasswordNotSet

        try:
            return super().validate(attrs)
        except AuthenticationFailed:
            raise exceptions.UserCredentialsInvalid
