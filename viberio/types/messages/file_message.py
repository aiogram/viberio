import attr

from .message import TypedMessage


@attr.s
class FileMessage(TypedMessage):
    type: str = attr.ib(default='file')
    media: str = attr.ib(default=None)
    size: str = attr.ib(default=None)
    file_name: str = attr.ib(default=None)
