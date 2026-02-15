from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Ad
from .serializers import AdSerializer
from core.pagination import Pagination
from core.permissions import IsOwnerOrReadOnly


# Create your views here.
class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['creator', 'category']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
