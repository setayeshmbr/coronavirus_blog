from django.urls import path

from blog.views import CategoryList, ArticleList, ArticleDetail, AuthorList, ArticlePreview

app_name ='blog'
urlpatterns =[
    path('' , ArticleList.as_view() , name ='home'),

    path('article/<slug:slug>' , ArticleDetail.as_view() , name ='detail'),
    path('article/preview/<int:pk>/' , ArticlePreview.as_view() , name ='preview'),

    path('category/<slug:slug>' , CategoryList.as_view() , name ='category'),
    path('author/<slug:username>' , AuthorList.as_view() , name ='author'),
]