import attr

from viberio.types.base import ViberBaseObject


@attr.s
class Message(ViberBaseObject):
    tracking_data: str = attr.ib(default=None)
    keyboard: str = attr.ib(default=None)
    min_api_version: str = attr.ib(default=None)
    alt_text: str = attr.ib(default=None)


@attr.s
class TypedMessage(Message):
    type: str = attr.ib(default=None)
