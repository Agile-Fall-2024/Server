from urllib.parse import urlparse

from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models.fields.files import ImageFieldFile
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.settings import api_settings

class FileSerializer(serializers.BaseSerializer):
    default_error_messages = {
        'invalid': _(
            'Upload a valid image. The file you uploaded was either not an image or a corrupted image.'
        ),
    }

    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail('invalid')

        path = urlparse(data).path.removeprefix(settings.MEDIA_URL)
        if not default_storage.exists(path):
            self.fail('invalid')
        return path

    def to_representation(self, value):
        if not value:
            return None
        if not isinstance(value, ImageFieldFile):
            return value

        use_url = getattr(self, 'use_url', api_settings.UPLOADED_FILES_USE_URL)
        if use_url:
            try:
                url = value.url
            except AttributeError:
                return None
            request = self.context.get('request', None)
            if request is not None:
                return request.build_absolute_uri(url)
            return url

        return value.name

