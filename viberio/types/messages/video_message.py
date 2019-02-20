import attr

from .message import TypedMessage


@attr.s
class VideoMessage(TypedMessage):
    type: str = attr.ib(default='video')
    media: str = attr.ib(default=None)
    thumbnail: str = attr.ib(default=None)
    size: str = attr.ib(default=None)
    duration: str = attr.ib(default=None)
    text: str = attr.ib(default=None)
