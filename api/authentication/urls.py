from django.urls import path
from .views import OtpVerify, RegisterNumber

urlpatterns = [
    path("verify/", OtpVerify.as_view(), name="OTP verify"),
    path("phone/", RegisterNumber.as_view(), name="OTP Gen"),
]
