from rest_framework import serializers

from .models import Otp, CustomUser


class OtpVerifySerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=14)
    otp_number = serializers.IntegerField()

    class Meta:
        model = Otp
        fields = ['otp_number', 'phone_number']


class PhoneVerifySerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=14)

    class Meta:
        model = Otp
        fields = ['phone_number']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'
