from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    is_superuser = None
    is_staff = None

    phone_number = models.CharField(unique=True, max_length=14)
    email = models.EmailField(_('email address'), unique=True, null=True)
    password = models.CharField(null=True, max_length=255)
    address = models.CharField(null=True, max_length=255)
    is_web_user = models.BooleanField(default=False)
    is_profile_completed = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number


class Otp(models.Model):
    user_id = models.IntegerField()
    otp_number = models.IntegerField()
    is_sms_sent = models.BooleanField(default=False)
    sms_retry_count = models.IntegerField(default=0)
    expired_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['user_id', 'otp_number', 'expired_at']

    objects = CustomUserManager()

    def __str__(self):
        return self.otp_number
