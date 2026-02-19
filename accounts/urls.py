from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, SendOTPView, VerifyOTPView, LogoutView

router = DefaultRouter()
router.register(prefix=r'accounts', viewset=UserViewSet, basename='accounts')

authurlpatterns = [
    path("send-otp", SendOTPView.as_view(), name="send-otp"),
    path("verify-otp", VerifyOTPView.as_view(), name="verify-otp"),
path("logout", LogoutView.as_view(), name="logout"),
]

urlpatterns = authurlpatterns + router.urls

