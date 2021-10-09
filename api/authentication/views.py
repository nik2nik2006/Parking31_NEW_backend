import datetime
import random

from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, Otp
from .serializers import OtpVerifySerializer


class RegisterNumber(APIView, BaseBackend):
    authentication_classes = []

    @staticmethod
    def post(request, phone_number):
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except ObjectDoesNotExist:
            user = CustomUser.objects.create(phone_number=phone_number)

        Otp.objects.filter(user_id=user.id).update(is_active=False)

        otp_number = random.randint(1000, 9999)
        otp_expired_at = make_aware(datetime.datetime.now()) + datetime.timedelta(minutes=5)
        Otp.objects.create(
            user_id=user.id,
            otp_number=otp_number,
            expired_at=otp_expired_at
        )

        return Response(
            {
                "data": {
                    "result": {
                        "user_id": user.id,
                        "is_profile_completed": user.is_profile_completed,
                        "otp_expired_at": otp_expired_at
                    },
                    "message": "Otp created and will be sent shortly. Please wait."
                }
            }, status=status.HTTP_201_CREATED
        )


class OtpVerify(APIView):
    # permission_classes = (IsAuthenticated,)
    # permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @staticmethod
    def post(request):
        serializer = OtpVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "error": {
                        "code": 400,
                        "message": serializer.errors
                    }
                }, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = CustomUser.objects.get(phone_number=request.data['phone_number'])
        except ObjectDoesNotExist:
            return Response(
                {
                    "error": {
                        "code": 404,
                        "message": "Phone number not registered. Please register first."
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )

        try:
            otp = Otp.objects.get(otp_number=request.data['otp_number'])
        except ObjectDoesNotExist:
            return Response(
                {
                    "error": {
                        "code": 404,
                        "message": "Wrong otp number."
                    }
                }, status=status.HTTP_404_NOT_FOUND
            )

        if otp.is_active:
            if otp.expired_at >= make_aware(datetime.datetime.now()):
                otp.is_active = False
                otp.save()

                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "data": {
                            "result": {
                                "user_id": user.id,
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                                "is_profile_completed": user.is_profile_completed,
                            },
                            "message": "Otp verified successfully!"
                        }
                    }, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "error": {
                            "code": 400,
                            "message": "Otp number expired."
                        }
                    }, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {
                "error": {
                    "code": 400,
                    "message": "Invalid Otp number."
                }
            }, status=status.HTTP_400_BAD_REQUEST
        )
