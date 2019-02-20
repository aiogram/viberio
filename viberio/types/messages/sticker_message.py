import attr

from .message import TypedMessage


@attr.s
class StickerMessage(TypedMessage):
    type: str = attr.ib(default='sticker')
    sticker_id: str = attr.ib(default=None)
    media: str = attr.ib(default=None)
