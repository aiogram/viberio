import attr

from .message import TypedMessage


@attr.s
class TextMessage(TypedMessage):
    type: str = attr.ib(default='text')
    text: str = attr.ib(default=None)
