from django.contrib import admin

from blog.custom_site import custom_site
from blog.base_admin import BaseOwnerAdmin
from .models import Comment
import xadmin



@xadmin.sites.register(Comment)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')

