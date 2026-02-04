from rest_framework import serializers

from .models import Ad, AdImage
from users.serializers import UserSerializer


class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'image']


class AdSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    images = AdImageSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'

    def validate_images(self, value):
        if not (1 <= len(value) <= 5):
            raise serializers.ValidationError("Images must be between 1 and 5")
        return value
