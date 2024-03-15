from django.urls import path

from article import views

urlpatterns = [
    path('', views.create_article, name='create_article'),
    path('all/', views.all_articles, name='all_articles'),
]
