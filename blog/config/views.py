# from django.shortcuts import render 模板
from django.views.generic import ListView

from django.http import HttpResponse
from my_blog.views import CommonViewMixin
from .models import Link


class LinkListView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'

