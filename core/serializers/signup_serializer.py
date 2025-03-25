import re

from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import Group
from rest_framework import serializers


User = get_user_model()


class SignupUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    username = serializers.CharField(required=True)

    def validate_password(self, value):
        password_validation.validate_password(value, user=None)
        return value
    
    def validate_username(self, value):
        if not re.fullmatch(r'[A-Za-z0-9]+', value):
            raise serializers.ValidationError("Username can only contain alphanumeric characters.")
        if len(value) < 2:
            raise serializers.ValidationError("Username cannot be shorter than 2 characters.")
        return value
    
    def create(self, validated_data):
        user = super().create(validated_data)

        user.set_password(user.password)
        user.save()

        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
        )
