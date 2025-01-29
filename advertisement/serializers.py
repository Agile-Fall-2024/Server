from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from advertisement.models import Advertisement, Category, Report, Picture
from file.serializers import FileSerializer

class PictureSerializer(serializers.ModelSerializer):
    picture = FileSerializer()

    class Meta:
        model = Picture
        fields = ['picture',]

class AdvertisementSummarySerializer(serializers.ModelSerializer):
    favorite = serializers.SerializerMethodField(allow_null=True)
    main_picture = serializers.SerializerMethodField()

    def get_main_picture(self, obj):
        main_picture = obj.pictures.first()
        if not main_picture:
            return None
        return FileSerializer(main_picture.picture, context=self.context).data

    def get_favorite(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        account = user.account
        return account.favorite_advertisement.contains(obj)

    class Meta:
        model = Advertisement
        fields = ['id', 'author_id', 'title', 'main_picture', 'price', 'status', 'category', 'created_at', 'favorite']


class AdvertisementSerializer(serializers.ModelSerializer):
    favorite = serializers.SerializerMethodField()
    pictures = PictureSerializer(many=True)

    def get_favorite(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        account = user.account
        return account.favorite_advertisement.contains(obj)

    def validate_pictures(self, value):
        if not value:
            raise serializers.ValidationError(_('Pictures cannot be empty'))
        return value

    def create(self, validated_data):
        pictures_data = validated_data.pop('pictures')
        advertisement = Advertisement.objects.create(**validated_data)
        for picture_data in pictures_data:
            Picture.objects.create(advertisement=advertisement, **picture_data)
        return advertisement

    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ['author', ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['user', 'is_read', 'created_at']
