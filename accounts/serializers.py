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
        # Don't show this fields:
        fields = ('id', 'phone_number', 'username', 'created_at', 'updated_at')
        read_only_fields = ('id', 'phone_number', 'created_at', 'updated_at')
