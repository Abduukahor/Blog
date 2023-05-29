from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=30,
                             unique=True,
                             verbose_name='Название категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=150,
                             unique=True,
                             verbose_name='Заголовок статьи')
    content = models.TextField(verbose_name='Содержание статьи')
    photo = models.ImageField(upload_to='photos/',
                              null=True,
                              blank=True,
                              verbose_name='Фотография')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата обновления')
    publish = models.BooleanField(default=True,
                                  verbose_name='Статус статьи')
    views = models.IntegerField(default=0,
                                verbose_name='Просмотры')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://www.peerspace.com/resources/wp-content/uploads/2019/02/beverage-3157395_1280.jpg'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


'''Создать модель комментария, которая знает свою статью и пользователя
Также имеет поле текста и даты создания
Создать форму для комментария,
Выводить форму, к посту, только если пользователь зашел в аккаунт
Выводить комментарии в статью если они есть'''


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.article.title}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, default='Инфо о себе', verbose_name='О себе')
    photo = models.ImageField(upload_to='photos/profiles/',
                              null=True,
                              blank=True,
                              verbose_name='Фото')
    phone = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_photo(self):
        try:
            url = self.photo.url
        except:
            url = 'https://www.pngall.com/wp-content/uploads/5/Profile-PNG-Clipart.png'

        return url

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    like = models.BooleanField(default=False, verbose_name='Лайк')
    dislike = models.BooleanField(default=False, verbose_name='Дизлайк')

    def __str__(self):
        return f'{self.article.title} - {self.user.username} - {self.like} - {self.dislike}'

    class Meta:
        verbose_name = 'Лайк и дизлайк'
        verbose_name_plural = 'Лайки и дизлайки'
