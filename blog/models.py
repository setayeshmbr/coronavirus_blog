from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from account.models import User
from extensions.utils import jalali_converter
from .managers import ArticleManager, CategoryManager
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


class Category(models.Model):

    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name= 'children', verbose_name='زیر مجموعه')
    title = models.CharField(max_length=200 ,verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True,verbose_name='آدرس دسته بندی')
    status = models.BooleanField(default= True , verbose_name='آیا نمایش داده شود؟')
    position = models.IntegerField(verbose_name='پوزیشن', default=1)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural ='دسته بندی ها'
        ordering = ['parent__id','position']

    def __str__(self):
        return self.title

    objects = CategoryManager()


class Article(models.Model):

    STATUS_CHOICES  =(
        ('d', 'پیش نویس'),        # draft
        ('p', 'منتشر شده'),       # publish
        ('i', 'در حال بررسی'),    # investigation
        ('b', 'برگشت داده شده '), # back
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles',
                               verbose_name='نویسنده')
    title = models.CharField(max_length=200 , verbose_name= 'عنوان')
    slug = models.SlugField(max_length=100 , unique=True, verbose_name= 'آدرس مقاله')
    category = models.ManyToManyField(Category ,verbose_name= 'دسته بندی', related_name='articles')
    description = models.TextField( verbose_name= 'محتوا')
    thumbnail = models.ImageField(upload_to= 'images', verbose_name= 'تصور مقاله')
    publish = models.DateTimeField(default= timezone.now, verbose_name= 'زمان انتشار')
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now= True)
    is_special = models.BooleanField(default=False, verbose_name='مقاله ویژه')
    status  = models.CharField(max_length= 2 , choices= STATUS_CHOICES , verbose_name='وضعیت انتشار')
    comments = GenericRelation(Comment)


    class Meta:
        verbose_name ='مقاله'
        verbose_name_plural ='مقالات'
        ordering =['-publish']

    def get_absolute_url(self):
        return reverse('account:home')

    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_descriptions ='زمان انتشار'

    # def category_published(self):
    #     return self.category.filter(status=True)

    def category_to_str(self):
        return ','.join([category.title for category in self.category.active()])

    category_to_str.short_description = 'دست بندی'

    def thumbnail_tag(self):
        return format_html("<img width=100 height=75 style='border-radius : 5px;' src ='{}'> ".format(self.thumbnail.url))
    thumbnail_tag.short_description ='تصویر مقاله'

    def __str__(self):
        return self.title

    objects = ArticleManager()


