from typing import Literal

from bs4 import BeautifulSoup
import requests
from django.views.decorators.csrf import csrf_exempt
from djapy import djapify, SessionAuth
from djapy.pagination import paginate, OffsetLimitPagination
from djapy.schema import payload
from openai import OpenAI
from pydantic import HttpUrl

import env
from .models import Article
from .schema import ArticleSchema, MessageOut

client = OpenAI(api_key=env.OPEN_AI_API_KEY, organization=env.OPEN_AI_ORG)


@djapify(allowed_method="POST", auth=SessionAuth)
@csrf_exempt
def create_article(request, url: payload(HttpUrl)) -> {200: ArticleSchema, 400: MessageOut}:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string
        plain_text = soup.get_text()

        article = Article.objects.create(
            user=request.user,
            html_content=response.text,
            plain_text=plain_text,
            url=url,
            title=title
        )
        return article
    except requests.exceptions.RequestException as e:
        return 400, {
            'alias': 'web_fetch_error',
            'message': "An error occurred while trying to fetch the article. Please try again later.",
            'message_type': 'error'
        }


@djapify(allowed_method="GET", auth=SessionAuth)
@paginate(OffsetLimitPagination)
def all_articles(request, **kwargs) -> {200: list[ArticleSchema]}:
    articles = Article.objects.filter(user=request.user)
    return articles
