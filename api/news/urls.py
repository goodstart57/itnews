from django.urls import path

from news import views

urlpatterns = [
    path('articles/<str:ref_type>/', views.ref_article_view),
    path('articles/', views.article_view),
]