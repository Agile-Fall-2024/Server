import posixpath
from uuid import uuid4

from django.core.files.storage import default_storage
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

def pictures_path(_instance, filename):
    _, ext = posixpath.splitext(filename)
    safe_name = str(uuid4())
    return posixpath.join("pictures", "{}{}".format(safe_name, ext))

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class PictureUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer

    @swagger_auto_schema(
        request_body=FileUploadSerializer,
        responses={201: openapi.Response('File uploaded successfully', FileUploadSerializer)}
    )
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if file:
            fs = default_storage
            filename = fs.save(pictures_path(None, file.name), file)  # Save the file and get the filename
            file_url = fs.url(filename)

            return Response({'file_url': request.build_absolute_uri(file_url)}, status=status.HTTP_201_CREATED)

        return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)