from django.urls import path
from .views import *

urlpatterns = [
    # path('', index, name='index'),
    path('', ArticleList.as_view(), name='index'),
    # path('category/<int:category_id>/', category_page, name='category'),
    path('category/<int:category_id>/', ArticleListByCategory.as_view(), name='category'),
    # path('article/<int:article_id>/', article_detail, name='article'),
    path('article/<int:pk>/', ArticleDetail.as_view(), name='article'),
    path('about_dev/', about_dev, name='about_dev'),
    # path('add/', add_article, name='add')
    path('add/', NewArticle.as_view(), name='add'),
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]
