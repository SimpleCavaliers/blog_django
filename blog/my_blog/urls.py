from django.urls import path
from django.contrib.sitemaps import views as sitemap_views
from django.conf.urls import url

from .views import *
from my_blog.sitemap import PostSitemap
from my_blog.rss import LastestPostFeed
#from .functions_views import post_detail, post_list


# 也可以在每个应用中单独配置 应用的本地路由
# django2.2中的path是直接拼接字符串，不采用正则表达式
'''
下面的路径转换器在默认情况下是有效的：

str - 匹配除了 '/' 之外的非空字符串。如果表达式内不包含转换器，则会默认匹配字符串。
int - 匹配0或任何正整数。返回一个 int 。
slug - 匹配任意由 ASCII 字母或数字以及连字符和下划线组成的短标签。比如，building-your-1st-django-site 。
uuid - 匹配一个格式化的 UUID 。为了防止多个 URL 映射到同一个页面，必须包含破折号并且字符都为小写。比如，075194d3-6885-417e-a8a8-6c931e272f00。返回一个 UUID 实例。
path - 匹配非空字段，包括路径分隔符 '/' 。它允许你匹配完整的 URL 路径而不是像 str 那样只匹配 URL 的一部分。
'''
urlpatterns = [
    path('', IndexView.as_view(), name='index'),# 还有namespace,看文档
    path('category/<int:category_id>/', CategoryView.as_view(), name='category-list'),
    path('tag/<int:tag_id>/', TagView.as_view(), name='tag-list'),
    path('post/<int:post_id>.html', PostDetailView.as_view(), name='post-detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('author/<int:owner_id>/', AuthorView.as_view(), name='author'),
    path('rss|feed/', LastestPostFeed(), name="rss"),
    path('sitemap\.xml', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}), # 当网页数多时可以设置多级sitemap
]