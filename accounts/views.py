from random import randint

from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from .models import User, OTP
from ads.models import Ad
from ads.serializers import AdUserFreeSerializer
from .serializers import UserSerializer, SendOTPSerializer, VerifyOTPSerializer
from core.pagination import Pagination


# Create your views here.
class SendOTPView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SendOTPSerializer

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]

        code = randint(100000, 999999)

        OTP.objects.create(phone_number=phone_number, code=code)

        print(f"OTP for {phone_number}: {code}")

        return Response({"message": "OTP sent successfully"})


class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        code = serializer.validated_data["code"]

        otp = OTP.objects.filter(
            phone_number=phone_number,
            code=code,
            is_used=False,
            expires_at__gt=timezone.now(),
        ).last()

        if not otp:
            return Response(
                data={"error": "Invalid or expired OTP"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        otp.is_used = True
        otp.save()

        user, created = User.objects.get_or_create(phone_number=phone_number)

        refresh = RefreshToken.for_user(user)
        return Response(
            data={
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Pagination
    filter_backends = [SearchFilter]
    search_fields = ['username']

    @action(detail=True, methods=['get'])
    def ads(self, request, pk=None):
        user = self.get_object()
        ads = Ad.objects.filter(creator=user)
        page = self.paginate_queryset(ads)
        if page is not None:
            serializer = AdUserFreeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AdUserFreeSerializer(ads, many=True)
        return Response(serializer.data)
