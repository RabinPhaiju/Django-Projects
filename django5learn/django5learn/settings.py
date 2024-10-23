# Django 5.1.1.

from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / '.env'
load_dotenv(dotenv_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l^s(&&*aqq6&npm+mse(*o5*3xc8ypx$^*+poa)8ylb_g^j#v#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1','localhost',
    'testserver', # for shell
]


# Application definition
# TODO https://docs.djangoproject.com/en/5.1/topics/http/sessions/

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'polls.apps.PollsConfig',
    'sql_queries.apps.SqlQueriesConfig',
    'sql_manager.apps.SqlManagerConfig',
    'sql_raw.apps.SqlRawConfig',
    'topic_http.apps.TopicHttpConfig',
    'model_form.apps.ModelFormsConfig',
    'base.apps.BaseConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django5learn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'django5learn.wsgi.application'


# Database
# TODO https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# https://docs.djangoproject.com/en/5.1/topics/db/multi-db/

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }

    'default': {
        'ENGINE': os.getenv('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('SQL_DATABASE', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv("SQL_USER", "user"),
        'PASSWORD': os.getenv("SQL_PASSWORD", "password"),
        'HOST': os.getenv("SQL_HOST", "localhost"),
        'PORT': os.getenv('SQL_PORT', '5432'),
    }
}

# Authentication Default user model
# https://docs.djangoproject.com/en/5.1/topics/auth/customizing/
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-user-model.
# Note:
# If you’re in an existing project and you just want to add a couple of fields to User, it's easier and safer to use a UserProfile model with a one-to-one relationship with User.
# If you want to switch to a custom User model in an existing project, you can do so, but it requires extra steps (such as rolling back migrations and starting fresh with a custom user model), which can be complex depending on your database and migration history.
AUTH_USER_MODEL = 'base.User'

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    {
        'NAME': 'django5learn.validators.MinimumLengthValidator', 
          # Your custom validator
        'OPTIONS': {
            'min_length': 10,  # Example of setting a custom length
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Password hashers
# https://docs.djangoproject.com/en/5.1/topics/auth/passwords/
PASSWORD_HASHERS = [
    # "django5learn.hashers.MyPBKDF2PasswordHasher",

    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

# For debug_toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

TESTING = "test" in sys.argv
if not TESTING:
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        "debug_toolbar",
    ]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]



# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu' # TODO set TIME_ZONE to your time zone

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# STATIC_ROOT = BASE_DIR / "staticfiles" 

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media/photos'
MEDIA_URL = '/media/'

# login url -- override default(/accounts/login/) -- in redirect
LOGIN_URL = '/login/'