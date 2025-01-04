from django.urls import include, path
from rest_framework.routers import DefaultRouter

from advertisement.views import AdvertisementViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'advertisement', AdvertisementViewSet, basename='advertisement')
router.register(r'category', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]