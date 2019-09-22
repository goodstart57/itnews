import json

from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from IPython import embed

from news.models import (
    Article,
    Latest,
    Main,
    Theme,
)
from news.serializers import (
    ArticleSerializer,
    LatestSerializer,
    MainSerializer,
    ThemeSerializer,
)


def wrap_articles(articles):
    if not isinstance(articles, list):
        return [articles]
    return articles

def is_overlapped(Model, cond):
    print(f"is_overlapped>Model:{Model}, cond:{cond}, result:{Model.objects.filter(**cond).count() > 0}")
    return Model.objects.filter(**cond).count() > 0

def save_obj_with_serializer(Serializer, data):
    serializer = Serializer(data=data)

    if serializer.is_valid():
        obj = serializer.save()
        return obj

    return None

def save_article_theme(article, themes):
    if themes:
        for theme in themes:
            if is_overlapped(Theme, {"url": theme.get("url")}):
                theme_obj = Theme.objects.filter(url=theme.get("url")).first()
            else:
                theme_obj = save_obj_with_serializer(ThemeSerializer, theme)
            
            if isinstance(theme_obj, Theme):
                article.themes.add(theme_obj.id)
    
    return article

def save_article_with_serializer(article):
    themes = article.get("themes")
    if themes: article.pop("themes")

    serializer = ArticleSerializer(data=article)

    if serializer.is_valid():
        article_obj = serializer.save()
        print(f"id:{article_obj.id}, title:{article_obj.title}")
        return save_article_theme(article_obj, themes)

    return None

def save_articles(articles):
    saved_num = 0                                           # count

    for new_article in articles:
        if is_overlapped(Article, {"url": new_article.get("url")}):             # overlapped article
            continue

        if save_obj_with_serializer(ArticleSerializer, new_article):
            saved_num += 1
    
    return saved_num

@api_view(('GET', 'POST'))
def article_view(request):
    # METHOD: GET
    if request.method == 'GET':
        return Response(ArticleSerializer(Article.objects.all(), many=True).data)

    # METHOD: POST
    new_articles = request.POST.get('articles')             # read articles
    new_articles = json.loads(new_articles)                 # parsing json to list dict or dict
    new_articles = wrap_articles(new_articles)              # wrap articles
    saved_num    = save_articles(new_articles)

    return JsonResponse({'saved': saved_num, 'total': len(new_articles)})


@api_view(('GET', 'POST'))
def ref_article_view(request, ref_type):
    if ref_type == 'latest':
        Model, Serializer = Latest, LatestSerializer
    elif ref_type == 'main':
        Model, Serializer = Main, MainSerializer
    else:
        return JsonResponse({'msg': 'wrong article type name'})

    # METHOD: GET
    if request.method == 'GET':
        ref_articles = [
            get_object_or_404(Article, pk=article.get('article_id')).__dict__ 
            for article in Model.objects.values()
        ]

        return JsonResponse({'articles': ArticleSerializer(ref_articles, many=True).data})

    # METHOD: POST
    new_articles = request.POST.get('articles')             # read articles
    new_articles = json.loads(new_articles)                 # parsing json to list dict or dict
    new_articles = wrap_articles(new_articles)              # wrap articles
    saved_num    = save_articles(new_articles)

    for article in new_articles:
        url = article.get("url")
        Model(article=Article.objects.get(url=url)).save()

    return JsonResponse({'saved': saved_num, 'total': len(new_articles)})

