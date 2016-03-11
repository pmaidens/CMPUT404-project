"""
Django settings for BloggingAPI project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hxzm3as(en_2nuu&@o!%u79^zky-#w@uc34n6cbfdk36l@$8(q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOCAL_ENV=False

SITE_ID=1

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
	'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'django.contrib.sites',
    'rest_framework',
	'rest_framework.authtoken',
	'rest_auth',
	'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
    'BloggingAPI',
)

MIDDLEWARE_CLASSES = (

	'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = (
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS'
    )




#change this to url of frontend
#https://github.com/ottoyiu/django-cors-headers for more info


ROOT_URLCONF = 'BloggingAPI.urls'

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

WSGI_APPLICATION = 'BloggingAPI.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# if not LOCAL_ENV:
# 	DATABASES = {
#     		'default': {
#         		'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         		'NAME': 'project',
#         		'USER': os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
#         		'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
#         		'HOST': os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
#         		'PORT': os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
#     		}
# 	}
# else:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'project',
        'USER': 'adminux1q3pu',
        'PASSWORD': 'DZzjTF25jQMV',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'BloggingAPI', 'static')
STATIC_DIRS = (
    os.path.join(BASE_DIR, "BloggingAPI/static"),
    # os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'], '/virtenv/lib/python2.7/site-packages/rest_framework/static')

)


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.BasicAuthentication',
# 		'rest_framework.authentication.TokenAuthentication',
#     ),
# 	'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
# }

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
