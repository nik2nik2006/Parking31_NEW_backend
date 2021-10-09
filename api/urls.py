from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .user_profile.views import UserProfileView

urlpatterns = [
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', include('api.authentication.urls')),
    path('api/otp/', include('api.authentication.urls')),
    path('api/profile', UserProfileView.as_view(), name="user_profile"),
]
