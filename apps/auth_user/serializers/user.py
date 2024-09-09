from rest_framework import serializers

from ..models import User


class CreateUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'password', 'is_staff', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True}
        }


class UpdateUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'mobile_phone', 'birth_date', 'is_staff', 'is_active')
        extra_kwargs = {
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True}
        }


class UserActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField()


class UserPasswordResetSerializer(serializers.Serializer):
    activation_code = serializers.CharField()
    email = serializers.EmailField()


class UserPasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField()
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs


class UserForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField()
    new_password = serializers.CharField()
    new_password_confirm = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs
