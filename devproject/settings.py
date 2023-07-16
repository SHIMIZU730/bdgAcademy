
import os
from .settings_common import *

DEBUG = False

ALLOWED_HOSTS = [
    os.environ.get('ALLOWED_HOSTS'),
    os.environ.get('ALLOWED_HOSTS_DOMAIN'),
    os.environ.get('ALLOWED_HOSTS_DNS'),
    os.environ.get('ALLOWED_HOSTS_ALB_DNS'),
    os.environ.get('ALLOWED_HOSTS_PRI_IP'),
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}

GOOGLE_ANALYTICS_TRACKING_ID = os.environ.get('GA_ID')