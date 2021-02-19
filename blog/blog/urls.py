"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import xadmin

from .custom_site import custom_site
from .autocomplete import CategoryAutocomplete, TagAutocomplete


urlpatterns = [
    path('', include('my_blog.urls')),
    path('', include('config.urls')),
    path('', include('comment.urls')),
    path('category-autocomplete/', CategoryAutocomplete.as_view(),
         name='category-autocomplete'),
    path('tag-autocomplete/', TagAutocomplete.as_view(), name='tag-autocomplete'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', xadmin.site.urls, name='xadmin'),
    # path('admin/', custom_site.urls, name='admin'),
    path('super_admin/', admin.site.urls, name='super-admin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 正式环境中要用NGINX完成静态资源服务(static)
