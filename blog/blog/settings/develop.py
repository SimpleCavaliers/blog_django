# flake8: NOQA
from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'yufeng_son',
        'PASSWORD': '@LIwenjing1998',
        'HOST': 'rm-bp1c464r0ra33fy43wo.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB',
        }
    }
}