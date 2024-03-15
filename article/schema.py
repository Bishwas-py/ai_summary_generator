from typing_extensions import TypedDict
from typing import Literal, Optional
from djapy import Schema


class ArticleSchema(Schema):
    id: int
    html_content: str
    plain_text: str
    url: str
    title: str
    summary: Optional[str] = None


class MessageOut(TypedDict):
    alias: str
    message: str
    message_type: Literal['error', 'info', 'success', 'warning']
