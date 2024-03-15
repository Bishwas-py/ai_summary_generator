from django.contrib import admin

from article.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass
