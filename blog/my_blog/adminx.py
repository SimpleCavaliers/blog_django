from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.admin.models import LogEntry

import xadmin
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter
from xadmin.layout import Row, Fieldset, Container
from blog.custom_site import custom_site
from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from blog.base_admin import BaseOwnerAdmin


# 内置的编辑相关内容更适合字段少的Model。这里演示一下。为伪需求。
# 在category中添加inlines = [PostInline, ]
# class PostInline(admin.TabularInline): # StackedInline 样式不同
#     fields = ('title', 'desc')
#     extra = 1 # 控制额外多几个
#     model = Post

# 使用xadmin
# class PostInline:
#     form_layout = (
#         Container(
#             Row("title", "desc"),
#         )
#     )
#     extra = 1
#     model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):

    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'
    # 显示实例化的类名，而不是category object



@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(RelatedFieldListFilter):

    # 类展示的过滤器
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user). \
            values_list('id', 'name')

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status','owner',
        'created_time', 'operator', 'tag'
    ]
    list_display_links = []

    # 只展现自己创建的分类
    list_filter = ['category']
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    #编辑页面
    save_on_top = True
    form_layout = (
        Fieldset('基础配置',
                 Row('title', 'category'),
                 'status',
                 'tag'
                 ),
        Fieldset('内容信息',
                'desc',
                'content',
                 ),
    )


    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:my_blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    # 实现自定义静态资源引入
    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/"
    #                 "bootstrap.min.css",),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )
    @property
    def mdedia(self):
        # xadmin基于Bootstrap，引入会导致页面样式冲突，这里只做演示
        media = super().media
        media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
        media.add_css({'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/"
                       "bootstrap.min.css",),})
        return media


# 展示log(xadmin中自带，去掉)
# @admin.register(LogEntry)
# class LogEntryAdmin(BaseOwnerAdmin):
#     list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']