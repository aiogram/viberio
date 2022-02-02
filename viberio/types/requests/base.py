import attr

from viberio.types.base import ViberBaseObject


@attr.s
class ViberRequestObject(ViberBaseObject):
    event: str = attr.ib()
    chat_hostname: str = attr.ib()
    timestamp: int = attr.ib()
    message_token: int = attr.ib()
