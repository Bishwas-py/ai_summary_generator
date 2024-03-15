from typing_extensions import TypedDict
from typing import Literal
from djapy import Schema


class ArticleSchema(Schema):
    html_content: str
    plain_text: str
    url: str
    title: str


class MessageOut(TypedDict):
    alias: str
    message: str
    message_type: Literal['error', 'info', 'success', 'warning']
