# flake8: noqa
import sys
# import dj_database_url
import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.conf import settings


# def get_env_data_as_dict(path: str) -> dict:
#     with open(path, 'r') as f:
#         return dict(tuple(line.replace('\n', '').split('=')) for line in f.readlines() if not line.startswith('#'))


# vars_dict = get_env_data_as_dict('.env')
# os.environ.update(vars_dict)

BASE_DIR = Path(__file__).resolve().parent.parent

DEVELOPMENT_MODE = True
# DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-8#ccs1y4&&3xr^ume^9$mcfty@$&)*p!7i&m$+d-zjg3#&&5a4")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", default=True)

# ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", ['localhost', '127.0.0.1', '0.0.0.0'])
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres', #это модуль Django, который предоставляет интеграцию с базой данных PostgreSQL 
    'corsheaders',
    'rest_framework',
    'djoser',
    'rest_framework_simplejwt',
    # 'storages',
    'api.authentication',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if DEVELOPMENT_MODE is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
    'default': {
        # Меняем настройку Django: теперь для работы будет использоваться
        # бэкенд postgresql
        'ENGINE': 'django.db.backends.postgresql',   # Используется PostgreSQL
        'NAME': 'postgres', # Имя базы данных
        'USER': 'postgres', # Имя пользователя
        'PASSWORD': 'postgres', # Пароль пользователя
        # 'HOST': 'pgdb', # Наименование контейнера для базы данных в Docker Compose
        'HOST': 'localhost', # изменил на локальном компьютере через pgAdmin
        'PORT': '5432',  # Порт базы данных
    }
}
    
# elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
#     if os.environ.get('DATABASE_URL', None) is None:
#         raise Exception('DATABASE_URL environment variable not defined')
#     DATABASES = {
#         'default': dj_database_url.parse(os.environ.get('DATABASE_URL')),
#     }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


if DEVELOPMENT_MODE is True:
    STATIC_URL = '/static/'
    SATTIC_ROOT = BASE_DIR / 'static'
    MEDIA_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    STATIC_URL = '/static/'
    SATTIC_ROOT = BASE_DIR / 'static'
    MEDIA_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authentication.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.authentication.authentication.CustomJWTAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',  
    # ],
    'EXCEPTION_HANDLER': 'api.authentication.exceptions.custom_exception_handler',
}

DJOSER = {
    # 'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    # 'SEND_ACTIVATION_EMAIL': True,
    # 'ACTIVATION_URL': 'activate/{uid}/{token}',
    # 'USER_CREATE_PASSWORD_RETYPE': True,
    # 'PASSWORD_RESET_CONFIRM_RETYPE': True,
    # 'TOKEN_MODEL': None,
}

AUTH_COOKIE = 'access'
AUTH_COOKIE_ACCESS_MAX_AGE = 60 * 5
AUTH_COOKIE_REFRESH_MAX_AGE = 60 * 60 * 24 * 180
AUTH_COOKIE_SECURE = os.getenv('AUTH_COOKIE_SECURE', 'True') == 'True'
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_PATH = '/'
AUTH_COOKIE_SAMESITE = 'None'

CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', "http://localhost:3000,http://127.0.0.1:3000").split(",")
CORS_ALLOW_CREDENTIALS = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
