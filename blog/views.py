from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from account.mixins import AuthorAccessMixin
from account.models import User
from blog.models import Article, Category


class ArticleList(ListView) :
    # model = Article
    queryset = Article.objects.published()
    paginate_by = 3


class ArticleDetail(DetailView) :
    def get_object(self, queryset=None) :
        slug = self.kwargs.get('slug')
        article =get_object_or_404(Article.objects.published(), slug=slug)
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



# def home(request):
#     article_list = Article.objects.published()
#     paginator = Paginator(article_list , 3)
#     page = request.GET.get('page')
#     articles = paginator.get_page(page)
#     context ={
#         'articles': articles,
#     }
#     return render(request, 'blog/home.html' , context)


# def detail (request ,slug):
#     context = {
#         'article': get_object_or_404(Article.objects.published(), slug=slug)
#     }
#     return render(request, 'blog/article_detail.html', context)


# def category(request, slug):
#     category =  get_object_or_404(Category, slug=slug, status=True)
#     article_list = category.articles.published()
#
#     paginator = Paginator(article_list, 3)
#     page = request.GET.get('page')
#     articles = paginator.get_page(page)
#     context = {
#         'category' : category,
#         'articles' : articles
#     }
#     return render(request, 'blog/home.html', context)
