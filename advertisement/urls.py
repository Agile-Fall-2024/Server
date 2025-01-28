from django.urls import include, path
from rest_framework.routers import DefaultRouter

from advertisement.views import AdvertisementViewSet, CategoryViewSet, ReportViewSet

router = DefaultRouter()
router.register(r'advertisement', AdvertisementViewSet, basename='advertisement')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'report', ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]
