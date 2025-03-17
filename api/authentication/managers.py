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
