from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Ad, Bookmark
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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_bookmark(self, request, pk=None):
        ad = self.get_object()
        user = request.user

        bookmark_qs = Bookmark.objects.filter(user=user, ad=ad)

        if bookmark_qs.exists():
            bookmark_qs.delete()
            return Response({"message": "Bookmark removed"}, status=status.HTTP_200_OK)

        Bookmark.objects.create(user=user, ad=ad)
        return Response({"message": "Bookmarked successfully"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_bookmarks(self, request):
        bookmarks = Bookmark.objects.filter(user=request.user).select_related('ad')
        ads = [bookmark.ad for bookmark in bookmarks]

        page = self.paginate_queryset(ads)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(ads, many=True)
        return Response(serializer.data)
