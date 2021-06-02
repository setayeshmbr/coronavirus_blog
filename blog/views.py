from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from account.mixins import AuthorAccessMixin
from account.models import User
from blog.models import Article, Category
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings

CACHE_TTL  =  getattr(settings , 'CACHE_TTL' ,DEFAULT_TIMEOUT )

class ArticleList(ListView) :
    # model = Article
    queryset = Article.objects.published()
    paginate_by = 3


class ArticleDetail(DetailView) :
    def get_object(self, queryset=None) :
        slug = self.kwargs.get('slug')
        if cache.get(slug):
            print("data from cacheeeeeeeeeeee*********")
            article = cache.get(slug)
        else:
            try:
                article =get_object_or_404(Article.objects.published(), slug=slug)
                cache.set(slug, article)
                print("data from databaseeeeeeeeeeeeeeeeeeeee **********")
            except Article.DoesNotExist:
                return redirect('/')


        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)
        return article


class ArticlePreview(AuthorAccessMixin, DetailView) :
    def get_object(self, queryset=None) :
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


class CategoryList(ListView) :
    template_name = 'blog/category_articles_list.html'
    paginate_by = 3

    def get_queryset(self) :
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()

    def get_context_data(self, *, object_list=None, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView) :
    template_name = 'blog/author_list.html'
    paginate_by = 3

    def get_queryset(self) :
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articles.published()

    def get_context_data(self, *, object_list=None, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context

