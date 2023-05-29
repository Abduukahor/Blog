from django.shortcuts import render, redirect
from .models import *
from .forms import ArticleForm
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy


# Create your views here.

# def index(request):
#     articles = Article.objects.all()
#     context = {
#         'title': 'Главная страница',
#         'articles': articles
#     }
#     return render(request, 'blog/index.html', context)


class ArticleList(ListView):
    model = Article  # Указываем что вытаскивать и откуда вытаскивать
    context_object_name = 'articles'
    template_name = 'blog/index.html'
    extra_context = {
        'title': 'Главная страница'
    }

    def get_queryset(self):
        articles = Article.objects.all()
        return articles


# def category_page(request, category_id):
#     articles = Article.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'title': f'Категория: {category.title}',
#         'articles': articles
#     }
#     return render(request, 'blog/index.html', context)

class ArticleListByCategory(ArticleList):
    def get_queryset(self):
        articles = Article.objects.filter(category_id=self.kwargs['category_id'])
        return articles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['category_id'])
        context['title'] = f"Статья категории: {category.title}"
        return context


# def article_detail(request, article_id):
#     article = Article.objects.get(pk=article_id)
#     article.views += 1
#     article.save()
#     articles = Article.objects.all()
#     articles = articles.order_by('-views')
#     context = {
#         'article': article,
#         'articles': articles[:5]
#     }
#
#     return render(request, 'blog/article_detail.html', context)

class ArticleDetail(DetailView):
    model = Article

    def get_queryset(self):
        return Article.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        article.views += 1
        article.save()
        context['title'] = f"Статья на тему: {article.title}"
        articles = Article.objects.all()
        articles = articles.order_by('-views')
        context['articles'] = articles[:4]
        return context


def about_dev(request):
    return render(request, 'blog/about_dev.html')


# def add_article(request):
#     if request.method == 'POST':
#         form = ArticleForm(request.POST, request.FILES)
#         if form.is_valid():
#             article = Article.objects.create(**form.cleaned_data)
#             article.save()
#             return redirect('article', article.pk)
#     else:
#         form = ArticleForm()
#
#     context = {
#         'form': form,
#         'title': 'Добавить статью'
#     }
#
#     return render(request, 'blog/article_form.html', context)

class NewArticle(CreateView):
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    extra_context = {
        'title': 'Добавить новую статью '
    }


class ArticleUpdate(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'

class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('index')
    context_object_name = 'article'