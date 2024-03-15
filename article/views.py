from typing import Literal

from bs4 import BeautifulSoup
import requests
from django.views.decorators.csrf import csrf_exempt
from djapy import Schema, djapify, SessionAuth
from djapy.pagination import paginate, OffsetLimitPagination
from djapy.schema import payload
from pydantic import HttpUrl
from typing_extensions import TypedDict

from .models import Article


class ArticleSchema(Schema):
    html_content: str
    plain_text: str
    url: str
    title: str


class MessageOut(TypedDict):
    alias: str
    message: str
    message_type: Literal['error', 'info', 'success', 'warning']


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
