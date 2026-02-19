from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from .models import User, OTP
from ads.models import Ad
from ads.serializers import AdUserFreeSerializer
from .serializers import UserSerializer, SendOTPSerializer, VerifyOTPSerializer
from core.pagination import Pagination
from .services.otp import OTPService


# Create your views here.
class SendOTPView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SendOTPSerializer

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        otp_service = OTPService()

        OTP.objects.filter(
            phone_number=phone_number,
            is_used=False,
            expires_at__gt=timezone.now(),
        ).update(is_used=True)

        code = otp_service.generate_code()
        salt = otp_service.generate_salt()
        code_hash = otp_service.hash_code(code=code, salt=salt)
        expires_at = otp_service.expires_at()

        OTP.objects.create(
            phone_number=phone_number,
            code_hash=code_hash,
            salt=salt,
            expires_at=expires_at,
        )

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
            is_used=False,
            expires_at__gt=timezone.now(),
        ).order_by("-created_at").first()

        if not otp:
            return Response(
                {"error": "Invalid or expired OTP"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if otp.attempts >= 5:
            return Response(
                {"error": "Too many attempts"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp_service = OTPService()

        is_valid = otp_service.verify_code(
            code=code,
            salt=otp.salt,
            code_hash=otp.code_hash,
        )

        if not is_valid:
            otp.attempts += 1
            otp.save(update_fields=["attempts"])
            return Response(
                {"error": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp.is_used = True
        otp.save(update_fields=["is_used"])

        user, created = User.objects.get_or_create(phone_number=phone_number)

        refresh = RefreshToken.for_user(user)

        return Response(
            data={
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
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

    @action(detail=False, methods=['get', 'patch', 'put'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        # If PUT or PATCH
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Token is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"error": "Malformed request"}, status=status.HTTP_400_BAD_REQUEST)