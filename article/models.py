from django.contrib.auth import get_user_model
from django.db import models


class Article(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    html_content = models.TextField()
    plain_text = models.TextField()
    url = models.URLField()
    title = models.CharField(max_length=200)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
