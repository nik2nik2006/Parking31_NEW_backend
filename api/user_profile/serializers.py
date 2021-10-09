from rest_framework import serializers

from ..authentication.models import CustomUser


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    address = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=254)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'address']
