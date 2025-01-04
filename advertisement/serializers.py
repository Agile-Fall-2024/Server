from rest_framework import serializers

from advertisement.models import Advertisement, Category, Report


class AdvertisementSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id', 'author_id', 'title', 'main_picture', 'price', 'status', 'category', 'created_at']


class AdvertisementSerializer(serializers.ModelSerializer):
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
        read_only_fields = ['is_read', 'created_at']
