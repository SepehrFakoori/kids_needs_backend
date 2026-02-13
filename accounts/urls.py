from rest_framework.routers import DefaultRouter

from .views import AccountViewSet

router = DefaultRouter()
router.register(prefix=r'accounts', viewset=AccountViewSet, basename='accounts')

urlpatterns = router.urls
