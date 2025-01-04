from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from advertisement.filters import IsAuthorFilterBackend, PriceFilterBackend, CategoryFilterBackend
from advertisement.models import Advertisement, Category
from advertisement.permissions import IsAuthorOrAdmin
from advertisement.serializers import AdvertisementSummarySerializer, AdvertisementSerializer, CategorySerializer

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthorOrAdmin]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        IsAuthorFilterBackend,
        PriceFilterBackend,
        CategoryFilterBackend,
    ]
    search_fields = ['title','description']
    ordering_fields = ['created','price']

    def get_serializer_class(self):
        if self.action == 'list':
            return AdvertisementSummarySerializer
        return AdvertisementSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [AllowAny()]
        return [IsAuthorOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
