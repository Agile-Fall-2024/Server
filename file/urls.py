from django.urls import path

from .views import PictureUploadView

urlpatterns = [
    path('picture', PictureUploadView.as_view(), name='picture'),
]
