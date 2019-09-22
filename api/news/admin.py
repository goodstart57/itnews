from django.contrib import admin

from news import models

@admin.register(models.Theme)
class ThemeModelAdmin(admin.ModelAdmin):
    list_display = tuple(map(lambda x: x.name, models.Theme._meta.fields))


@admin.register(models.Article)
class ArticleModelAdmin(admin.ModelAdmin):
    list_display = tuple(map(lambda x: x.name, models.Article._meta.fields))


@admin.register(models.Latest)
class LatestModelAdmin(admin.ModelAdmin):
    list_display = tuple(map(lambda x: x.name, models.Latest._meta.fields))


@admin.register(models.Main)
class MainModelAdmin(admin.ModelAdmin):
    list_display = tuple(map(lambda x: x.name, models.Main._meta.fields))
