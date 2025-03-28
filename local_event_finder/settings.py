import os
from pathlib import Path

# প্রজেক্টের বেস ডিরেক্টরি
BASE_DIR = Path(__file__).resolve().parent.parent

# সিক্রেট কী (পরে .env ফাইলে রাখার পরামর্শ)
SECRET_KEY = 'your-secret-key-here'


# ডেভেলপমেন্ট মোডে DEBUG চালু
DEBUG = True

# হোস্ট সেটিংস
ALLOWED_HOSTS = []

# ইনস্টল করা অ্যাপস
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events.apps.EventsConfig',
]

# মিডলওয়্যার
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL কনফিগারেশন
ROOT_URLCONF = 'local_event_finder.urls'

# টেমপ্লেট সেটিংস
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

# WSGI অ্যাপ্লিকেশন
WSGI_APPLICATION = 'local_event_finder.wsgi.application'

# ডাটাবেস
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# অথেনটিকেশন সেটিংস
LOGIN_URL = '/accounts/login/'  # Django-এর ডিফল্ট লগইন URL
LOGIN_REDIRECT_URL = '/'  # লগইনের পর রিডাইরেক্ট
LOGOUT_REDIRECT_URL = '/'  # লগআউটের পর রিডাইরেক্ট

# স্ট্যাটিক ফাইল সেটিংস
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # প্রজেক্টের রুটে static/ ফোল্ডার
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # কালেক্টস্ট্যাটিকের জন্য

# মিডিয়া ফাইল সেটিংস (ইমেজ আপলোডের জন্য)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ইমেইল সেটিংস (পাসওয়ার্ড রিসেটের জন্য)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # আপনার Gmail ঠিকানা
EMAIL_HOST_PASSWORD = 'your-app-password'  # Gmail App Password

# ভাষা এবং সময় সেটিংস (ঐচ্ছিক, তবে ভালো প্র্যাকটিস)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ডিফল্ট প্রাইমারি কী ফিল্ড টাইপ
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Stripe settings
STRIPE_SECRET_KEY = 'sk_test_51R6wOf74mjbq4tYIPL7uGBNPUAGOwjCDV9vwFExJMV3qpn3JyU4i1lOE71zBgNoCO3HGtMmbezBoIbLCqXcxoybm00mpfRYAvo'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51R6wOf74mjbq4tYIy3vLxZbTX96HajnfiUloofitMXPxeEJO5NEeap8TOthEf2GgIUn1zrqvFIyNDotAQOAAbJXx00NB5WosPw'