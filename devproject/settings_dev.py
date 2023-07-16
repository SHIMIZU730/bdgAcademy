
import os
from .settings_common import *

DEBUG = True
ALLOWED_HOSTS = [
    os.environ.get('ALLOWED_HOSTS')
]


# # # makemigrationを実施するときは、環境変数が反映されない可能性があるから、その場合は一旦ハードコーディングする。
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



