from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from .models import Account
from .serializers import AccountSerializer
from core.pagination import Pagination


# Create your views here.
class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    pagination_class = Pagination
    filter_backends = [SearchFilter]
    search_fields = ['username']
