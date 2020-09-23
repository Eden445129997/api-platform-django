#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import socket


# 别人的django代码
# git clone https://github.com/happyletme/requestnew.git

# 获取本机IP
def host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# LOGS_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%gv+a$_$rd9bof0(*sc4p!^(1ydra!h3l21+l@(bug$4j7@0nu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [host(), "127.0.0.1", "localhost"]

# Application definition
# 添加APP
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 跨域请求解决方案的跨域包
    "corsheaders",
    # drf框架（更加方便开发）
    "rest_framework",
    # demo服务
    # "apps.demo_service",
    # 测试服务
    "apps.qa_platform",
]

# drf 配置
REST_FRAMEWORK = {
    # AttributeError: 'AutoSchema' object has no attribute 'get_link'
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    # 新版drf自带文档接口配置
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 跨域设置（必须在django.middleware.csrf.CsrfViewMiddleware的上面）
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # csrf攻击跳过（前后端分离不需要做）
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # log中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定义中间件
    'apps.common.middleware.CustomMiddleware'
]

# 允许携带cookie
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# 允许跨域请求的白名单
# django3.0之后必须http开头
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8081',
    'http://localhost:8081'
)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
    'Access-Control-Allow-Origin',
)

# 根Url
ROOT_URLCONF = 'main.urls'

# 模板配置
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

WSGI_APPLICATION = 'main.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# pip install mysqlclient

# 如下报错：
# django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.3 or newer is required; you have 0.7.11.None
# 解决办法：
# 找到Python安装路劲下的Python36-32\Lib\site-packages\django\db\backends\mysql\base.py文件
# 将文件中的如下代码注释
# if version < (1, 3, 3):
#     raise ImproperlyConfigured("mysqlclient 1.3.3 or newer is required; you have %s" % Database.__version__)
# 重新在项目manage.py路劲下执行如下命令即可

# 如下报错：
# query = query.decode(errors='replace')
# AttributeError: 'str' object has no attribute 'decode'
# 解决方法：
# python3.6/site-packages/django/db/backends/mysql/operations.py
# 将decode改为encode

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "qa_platform",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "111.229.54.5",
        "PORT": 3306,
        # 配置长链接数
        # 'CONN_MAX_AGE': 5*60,
        "TEST": {
            'Name': 'djangotest',
            "CHARSET": "utf8",
            "COLLATION": "utf8_general_ci"
        }
    }
}

# 日志地址
LOG_DIR = os.path.join(BASE_DIR, 'logs')
# 如果不存该地址则创建
if not os.path.join(LOG_DIR):
    os.mkdir(LOG_DIR)

LOGGING = {
    # 版本
    'version': 1,
    # 是否禁止默认配置的记录器
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '\n%(asctime)s %(levelname)s\n'
                      '%(pathname)s\n'
                      'process_id:%(process)d\n'
                      'thread_id:%(thread)d\n'
                      '%(message)s\n',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    # 过滤器
    # 'filters': {
    #     'request_info': {'()': 'apps.common.custom_middleware.DataReCordMiddleware'},
    # },
    'handlers': {
        # 标准输出
        'console': {
            # 'level': 'DEBUG',
            'level': 'ERROR',
            # 'level': 'INFO',
            'class': 'logging.StreamHandler',
            # 'formatter': 'standard'
        },
        # 自定义 handlers，输出到文件
        'requests': {
            'level': 'DEBUG',
            # 时间滚动切分
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'http.log'),
            'encoding': 'utf-8',
            'formatter': 'standard',
            # 调用过滤器
            # 'filters': ['request_info'],
            # 每天凌晨切分
            # 'when': 'MIDNIGHT',
            # 保存 30 天
            # 'backupCount': 30,
        },
        # 自定义 handlers，输出到文件
        'event-api': {
            'level': 'DEBUG',
            # 时间滚动切分
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'event-api.log'),
            'encoding': 'utf-8',
            'formatter': 'standard',
            # 调用过滤器
            # 'filters': ['request_info'],
            # 每天凌晨切分
            # 'when': 'MIDNIGHT',
            # 保存 30 天
            # 'backupCount': 30,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'http': {
            'handlers': ['requests'],
            'level': 'INFO',
            'propagate': False
        },
        'event': {
            'handlers': ['event-api', 'console'],
            'level': 'INFO',
            # 此记录器处理过的消息就不再让 django 记录器再次处理了
            'propagate': False
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# 语言
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

# 时区
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

# 语言
USE_I18N = True

# 数据和时间格式
USE_L10N = True

# 启动时区
USE_TZ = True

# 设置用户模型（否则会用django自带的）
# AUTH_USER_MODEL = "user_service.User"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# 静态文件(STATICFILES_DIRS默认在公用文件中找，找不到就会在对应的app下找)
STATIC_URL = '/static/'
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
# print(os.path.join(BASE_DIR, 'logs/runner-log.log'))
