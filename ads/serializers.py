from rest_framework import serializers

from categories.serializers import CategorySerializer
from .models import Ad, AdImage, Bookmark
from accounts.serializers import UserSerializer


class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'image']


class AdSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    images = AdImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'

    def validate_images(self, value):
        if not (1 <= len(value) <= 5):
            raise serializers.ValidationError("Images must be between 1 and 5")
        return value

    def get_is_bookmarked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Bookmark.objects.filter(user=user, ad=obj).exists()
        return False


# For specific user ads
class AdUserFreeSerializer(serializers.ModelSerializer):
    images = AdImageSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        exclude = ('creator',)
