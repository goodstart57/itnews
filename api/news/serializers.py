from rest_framework import serializers
from news.models import Theme, Article, Latest, Main


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('name', 'url',)


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'content', 'date', 'url',)


class LatestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Latest
        fields = ('article',)


class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Latest
        fields = ('article',)
