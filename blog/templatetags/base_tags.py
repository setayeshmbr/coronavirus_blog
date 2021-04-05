from django import template

from blog.models import Category

register = template.Library()


@register.simple_tag
def title(data='وبلاگ جنگویی') :
    return data


@register.inclusion_tag('blog/partials/category_navbar.html')
def category_navbar() :
    context ={
        'categories' : Category.objects.filter(status=True)
    }
    return context



