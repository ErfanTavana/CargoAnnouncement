# این فایل settings.py شامل تنظیمات مربوط به پروژه Django شما است.

from pathlib import Path
import os
from pathlib import Path
from django.urls import path

# مسیر پایه پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

# کلید مخفی برای موارد حساس (مثل SECRET_KEY) - در محیط توسعه این مورد مهم نیست
SECRET_KEY = 'django-insecure-x+a_w2&j4@+%a9j=c&%4hryln@584$w%^1(#m0i^x0$77g4jv6'

# حالت اشکال‌زدایی - این مقدار در محیط توسعه باید True باشد
DEBUG = True

# لیست میزبان‌های مجاز برای دسترسی به سایت - در حالت توسعه، می‌تواند خالی باشد
ALLOWED_HOSTS = []

# افزونه‌های نصب‌شده در پروژه
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'carrier_owner',
    'carrier_owner_res',
    'driver',
    'driver_res',
    'goods_owner',
    'goods_owner_res',
    'ticket',
    'blog',
    'home',
    'CargoADMIN',

]

# میان‌افزارهای اجرایی برنامه
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF middleware before AuthenticationMiddleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
# تنظیمات پوشه‌ها و فایل‌ها
ROOT_URLCONF = 'CargoAnnouncement.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'CargoAnnouncement.wsgi.application'

# تنظیمات پایگاه داده
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# اعتبارسنجی رمز عبور
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

# تنظیمات زمان و تاریخ
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# تنظیمات فایل‌های استاتیک و رسانه‌ها
STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# تنظیمات REST framework برای استفاده از توکن برای احراز هویت
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# تنظیمات CORS برای اجازه دسترسی به API از دامنه‌های مشخص
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://127.0.0.1:3000',
    'http://localhost:3000',
]

# تنظیمات امان برای کوکی‌ها و سشن
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# زمینه پیشفرض برای مدل‌های جدید در Django 3.2+
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
