from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['phone_number', 'bio', 'address']

    def validate_phone_number(self, value):
        if value:
            account_id = self.instance.id if self.instance else None
            if Account.objects.exclude(id=account_id).filter(phone_number=value).exists():
                raise serializers.ValidationError(_("This phone number is already taken."))
        return value


class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'account']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("A user with that email already exists."))
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        account_data = validated_data.pop('account', {})

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        Account.objects.create(user=user, **account_data)
        return user
