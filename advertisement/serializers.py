from rest_framework import serializers

from advertisement.models import Advertisement, Category, Report
from file.serializers import FileSerializer


class AdvertisementSummarySerializer(serializers.ModelSerializer):
    favorite = serializers.SerializerMethodField(allow_null=True)
    main_picture = FileSerializer(required=True)

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
    main_picture = FileSerializer(required=True)

    def get_favorite(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        account = user.account
        return account.favorite_advertisement.contains(obj)

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
