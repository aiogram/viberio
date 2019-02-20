import attr

from .message import TypedMessage


@attr.s
class URLMessage(TypedMessage):
    type: str = attr.ib(default='url')
    media: str = attr.ib(default=None)
