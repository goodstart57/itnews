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



@api_view(('GET', 'POST'))
def ref_article_view(request, ref_type):
    if ref_type == 'latest':
        Model, Serializer = Latest, LatestSerializer
    elif ref_type == 'main':
        Model, Serializer = Main, MainSerializer
    else:
        return JsonResponse({'msg': 'wrong article type name'})

    if request.method == 'GET':
        ref_articles = [
            {
                'article': get_object_or_404(Article, pk=article.get('article_id')),
                'date': article.get('date').strftiem("%Y-%m-%d")
            } for article in Model.objects.values()
        ]

        return JsonResponse({'articles': ref_articles})
    # POST
    ref_articles = json.loads(request.POST.get('articles'))

    if not isinstance(ref_articles, list):
        ref_articles = [ref_articles]

    for ref_article in ref_articles:
        article = Article.objects.filter(url=ref_article.get('url'))
        saved_num = 0

        if article:
            article = article[0]
        else:
            themes = ref_article.pop('themes')
            article = Article(**ref_article)
            article.save()

            for theme in themes:
                theme = Theme.objects.get_or_create(**theme)
                article.themes.add(theme[0])

        serializer = Serializer(data={'article': article.id})
        if serializer.is_valid():
            serializer.save()
            saved_num += 1

    return JsonResponse({'saved': saved_num, 'total': len(ref_articles)})


@api_view(('GET', 'POST'))
def article_view(request):
    if request.method == 'GET':
        serializer = ArticleSerializer(
            Article.objects.all(),
            many=True
        )
        return Response(serializer.data)
    # POST
    new_articles = json.loads(request.POST.get('articles'))

    if not isinstance(new_articles, list):
        new_articles = [new_articles]

    for new_article in new_articles:
        article = Article.objects.filter(url=new_article.get('url'))
        saved_num = 0

        if article: # 중복 저장 방지
            continue

        serializer = ArticleSerializer(data=article)
        if serializer.is_valid():
            serializer.save()
            saved_num += 1

    return JsonResponse({'saved': saved_num, 'total': len(new_articles)})

