from django.urls import path

from .views import MainPictureUploadView, PictureUploadView

urlpatterns = [
    path('main-picture', MainPictureUploadView.as_view(), name='main-picture'),
    path('picture', PictureUploadView.as_view(), name='picture'),
]
