import datetime
import random

from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import make_aware, timedelta
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .models import CustomUser, Otp
from .serializers import (OtpVerifySerializer, PhoneVerifySerializer,
                          UserSerializer)


class RegisterNumber(APIView, BaseBackend):
    authentication_classes = []

    @staticmethod
    def post(request):
        serializer = PhoneVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "error": {
                        "code": 400,
                        "message": serializer.errors
                    }
                }, status=status.HTTP_400_BAD_REQUEST
            )
        print(request.data['phone_number'])
        try:
            user = CustomUser.objects.get(
                phone_number=request.data['phone_number'])
        except ObjectDoesNotExist:
            user = CustomUser.objects.create(
                phone_number=request.data['phone_number'])

        Otp.objects.filter(user_id=user.id).update(is_active=False)

        otp_number = random.randint(1000, 9999)
        otp_expired_at = make_aware(datetime.datetime.now())
        + datetime.timedelta(minutes=5)
        otp = Otp.objects.create(
            user_id=user.id,
            otp_number=otp_number,
            expired_at=otp_expired_at
        )
        return Response(
            {
                "data": {
                    "result": {
                        "otp": otp.otp_number,
                        "user_id": user.id,
                        "is_profile_completed": user.is_profile_completed,
                        "otp_expired_at": otp_expired_at
                    },
                    "message": "Otp created and will be sent shortly. \
                        Please wait."
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
            user = CustomUser.objects.get(
                phone_number=request.data['phone_number'])
        except ObjectDoesNotExist:
            return Response(
                {
                    "error": {
                        "code": 404,
                        "message": "Phone number not registered. \
                            Please register first."
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
        print('now= ', datetime.datetime.now())
        if otp.is_active:
            if otp.expired_at <= make_aware(datetime.datetime.now()):
                otp.is_active = False
                otp.save()

                refresh = RefreshToken.for_user(user)

                response = Response(
                    {
                        "user": UserSerializer(user).data,
                    }, status=status.HTTP_200_OK
                )
                response.set_cookie(
                    'access',
                    str(refresh.access_token),
                    expires=datetime.datetime.now() + timedelta(
                                 seconds=settings.AUTH_COOKIE_ACCESS_MAX_AGE),
                    path=settings.AUTH_COOKIE_PATH,
                    secure=settings.AUTH_COOKIE_SECURE,
                    httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                    samesite=settings.AUTH_COOKIE_SAMESITE
                )
                response.set_cookie(
                    'refresh',
                    str(refresh),
                    expires=datetime.datetime.now() + timedelta(
                                 seconds=settings.AUTH_COOKIE_REFRESH_MAX_AGE),
                    path=settings.AUTH_COOKIE_PATH,
                    secure=settings.AUTH_COOKIE_SECURE,
                    httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                    samesite=settings.AUTH_COOKIE_SAMESITE
                )

                return response
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


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                'access',
                access_token,
                expires=datetime.datetime.now() + timedelta(
                                seconds=settings.AUTH_COOKIE_ACCESS_MAX_AGE),
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')

        if access_token:
            request.data['token'] = access_token

        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
