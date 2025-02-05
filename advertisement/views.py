from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ReadOnlyModelViewSet

from advertisement.filters import IsAuthorFilterBackend, PriceFilterBackend, CategoryFilterBackend, \
    FavoriteFilterBackend
from advertisement.models import Advertisement, Category, Report
from advertisement.permissions import IsAuthorOrAdmin
from advertisement.serializers import AdvertisementSummarySerializer, AdvertisementSerializer, CategorySerializer, \
    ReportSerializer
from django.shortcuts import get_object_or_404


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
        FavoriteFilterBackend,
    ]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price']

    def get_serializer_class(self):
        if self.action == 'list':
            return AdvertisementSummarySerializer
        if self.action == 'add_favorite' or self.action == 'delete_favorite':
            return Serializer
        return AdvertisementSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [AllowAny()]
        if self.action == 'add_favorite' or self.action == 'delete_favorite':
            return [IsAuthenticated()]
        return [IsAuthorOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['put'], detail=True, description='add this advertisement to users favorite')
    def add_favorite(self, request, *args, **kwargs):
        advertisement = self.get_object()
        request.user.account.favorite_advertisement.add(advertisement)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['put'], detail=True)
    def delete_favorite(self, request, *args, **kwargs):
        advertisement = self.get_object()
        request.user.account.favorite_advertisement.remove(advertisement)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='owner-phone')
    def get_owner_phone(self, request, pk=None):
        advertisement = get_object_or_404(Advertisement, id=pk)
        owner_account = advertisement.author.account
        if not owner_account.phone_number:
            return Response(
                {"detail": "The owner has not provided a phone number."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({
            "ad_id": advertisement.id,
            "phone_number": owner_account.phone_number,
            "name": f"{owner_account.user.first_name} {owner_account.user.last_name}"
        },
            status=status.HTTP_200_OK
        )


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Report.objects.all()
        return Report.objects.filter(user=self.request.user)
