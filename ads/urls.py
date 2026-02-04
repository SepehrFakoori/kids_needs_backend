from rest_framework.routers import DefaultRouter

from .views import AdViewSet

router = DefaultRouter()
router.register(prefix=r'ads', viewset=AdViewSet, basename='ads')

urlpatterns = router.urls
