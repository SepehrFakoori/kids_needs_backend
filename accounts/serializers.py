from rest_framework import serializers

from .models import User


class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        # Don't show this fields:
        exclude = ('is_superuser', 'is_active', 'is_staff', 'groups', 'user_permissions')
