from django.urls import path, include, re_path
# from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from api.authentication.views import (
     CustomTokenRefreshView,
     CustomTokenVerifyView,
     LogoutView
     )


urlpatterns = [
    path('api/token/refresh/',
         CustomTokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/token/verify/',
         CustomTokenVerifyView.as_view(),
         name='token_verify'),
    path('logout/',
         LogoutView.as_view(),
         name='logout'),
    path('api/otp/', include('api.authentication.urls')),
    re_path(r'^auth/', include('djoser.urls')),
]
