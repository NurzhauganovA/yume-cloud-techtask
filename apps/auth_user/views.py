from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers.jwt import CustomTokenObtainPairSerializer
from .serializers.user import CreateUserRegisterSerializer, UserActivationSerializer, \
    UserPasswordResetSerializer, UpdateUserRegisterSerializer, UserPasswordResetConfirmSerializer, \
    UserForgotPasswordSerializer, UserChangePasswordSerializer
from .services import UserActivateService, UserPasswordResetService, \
    UserPasswordResetConfirmService, UserForgotPasswordService, UserChangePasswordService


class UserLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserRegisterSerializer

    def perform_create(self, serializer):
        serializer.save()


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserRegisterSerializer
    lookup_field = 'id'
    http_method_names = ['patch']

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserActivationView(generics.GenericAPIView):
    serializer_class = UserActivationSerializer
    user_activate_service = UserActivateService

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_activate_service = self.user_activate_service(
            email=serializer.data['email'],
            activation_code=int(serializer.data['activation_code'])
        )

        try:
            user_activate_service.activate_user()
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'User activated'}, status=status.HTTP_200_OK)


class UserPasswordResetView(generics.GenericAPIView):
    serializer_class = UserPasswordResetSerializer
    user_password_reset_service = UserPasswordResetService

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_password_reset_service = self.user_password_reset_service(
            email=serializer.data['email'],
            activation_code=int(serializer.data['activation_code']),
        )

        try:
            user_password_reset_service.reset_password()
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Sent password reset code'}, status=status.HTTP_200_OK)


class UserPasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = UserPasswordResetConfirmSerializer
    user_password_reset_service = UserPasswordResetConfirmService

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_password_reset_service = self.user_password_reset_service(
            email=serializer.data['email'],
            activation_code=int(serializer.data['activation_code']),
            password_confirm=serializer.data['password_confirm']
        )

        try:
            user_password_reset_service.reset_password_confirm()
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Password reset'}, status=status.HTTP_200_OK)


class UserForgotPasswordView(generics.GenericAPIView):
    serializer_class = UserForgotPasswordSerializer
    user_forgot_password_service = UserForgotPasswordService

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_forgot_password_service = self.user_forgot_password_service(
            email=serializer.data['email']
        )

        try:
            user_forgot_password_service.forgot_password()
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Sent password change code'}, status=status.HTTP_200_OK)


class UserChangePasswordView(generics.GenericAPIView):
    serializer_class = UserChangePasswordSerializer
    user_change_password_service = UserChangePasswordService

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_change_password_service = self.user_change_password_service(
            email=serializer.data['email'],
            activation_code=int(serializer.data['activation_code']),
            new_password_confirm=serializer.data['new_password_confirm']
        )

        try:
            user_change_password_service.change_password()
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Password changed'}, status=status.HTTP_200_OK)
