from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.admin.models import LogEntry

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


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):

    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'
    # 显示实例化的类名，而不是category object



@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    '''自定义过滤器只展示当前用户分类'''

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status','owner',
        'created_time', 'operator', 'tag'
    ]
    list_display_links = []

    # 只展现自己创建的分类
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    #编辑页面
    save_on_top = True
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述:',
            'fields':(
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        }),
    )


    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:my_blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    # 实现自定义静态资源引入
    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/"
    #                 "bootstrap.min.css",),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )


# 展示log
@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']