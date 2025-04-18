from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError(_('The phone must be set'))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_phone_number(phone_number)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if not phone_number:
            raise ValueError('The given phone must be set')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()

        return user
