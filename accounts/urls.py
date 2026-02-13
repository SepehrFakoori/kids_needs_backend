from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, SendOTPView, VerifyOTPView

router = DefaultRouter()
router.register(prefix=r'accounts', viewset=UserViewSet, basename='accounts')

authurlpatterns = [
    path("send-otp", SendOTPView.as_view(), name="send-otp"),
    path("verify-otp", VerifyOTPView.as_view(), name="verify-otp"),
]

urlpatterns = authurlpatterns + router.urls

