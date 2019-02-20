import attr

from .message import TypedMessage


@attr.s
class RichMediaMessage(TypedMessage):
    type: str = attr.ib(default='rich_media')
    rich_media: str = attr.ib(default=None)
    alt_text: str = attr.ib(default=None)
