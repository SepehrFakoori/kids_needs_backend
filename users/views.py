from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from .models import User
from .serializers import UserSerializer
from core.pagination import Pagination


# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Pagination
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']
