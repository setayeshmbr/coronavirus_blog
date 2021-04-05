from django.contrib import admin

from blog.models import Article, Category


# actions
def make_published(modeladmin, request, queryset) :
    row_updated = queryset.update(status='p')
    if row_updated == 1 :
        message_bit = 'منتشر شد.'
    else :
        message_bit = 'منتشر شدند.'
    modeladmin.message_user(request, '{} مقاله {}'.format(row_updated, message_bit))


make_published.short_description = 'انتشار مقالات انتخاب شده'


def make_draft(modeladmin, request, queryset) :
    row_updated = queryset.update(status='d')
    if row_updated == 1 :
        message_bit = 'پیش نویس شد.'
    else :
        message_bit = 'پیش نویس شدند.'
    modeladmin.message_user(request, '{} مقاله {}'.format(row_updated, message_bit))


make_draft.short_description = 'پیش نویس شدن مقالات انتخاب شده'


# registration
class CategoryAdmin(admin.ModelAdmin) :
    list_display = ['position', 'parent', 'title', 'slug', 'status']
    list_filter = ['status']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug' : ('title',)}
    ordering = ['-status']


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin) :
    list_display = ['title', 'thumbnail_tag', 'slug', 'publish', 'is_special', 'status', 'category_to_str']
    list_filter = ['publish', 'status']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug' : ('title',)}
    ordering = ['-status', 'publish']
    actions = [make_published, make_draft]


admin.site.register(Article, ArticleAdmin)

