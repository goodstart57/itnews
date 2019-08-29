from django.db import models
from django.utils import timezone

from datetime import datetime

class Theme(models.Model):
    name = models.CharField(max_length=20, default='')
    url = models.IntegerField(blank=True)
    following_themes = models.ManyToManyField('self', related_name='followed_themes', blank=True)

    __str__ = lambda self: self.name


class Article(models.Model):
    title = models.CharField(max_length=100, default='')
    content = models.TextField(default='')
    themes = models.ManyToManyField(Theme, related_name='theme_articles', blank=True)
    date = models.DateTimeField(default=datetime.now())
    url = models.IntegerField(blank=True)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    __str__ = lambda self: self.title


class Latest(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    __str__ = lambda self: self.article.title

class Main(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    __str__ = lambda self: self.article.title
    