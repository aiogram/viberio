import attr

from .message import TypedMessage


@attr.s
class PictureMessage(TypedMessage):
    type: str = attr.ib(default='picture')
    text: str = attr.ib(default=None)
    media: str = attr.ib(default=None)
    thumbnail: str = attr.ib(default=None)
    file_name: str = attr.ib(default=None)
