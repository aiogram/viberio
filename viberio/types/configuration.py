import attr

from viberio.types.base import ViberBaseObject


@attr.s
class BotConfiguration(ViberBaseObject):
    auth_token: str = attr.ib()
    name: str = attr.ib(default=None)
    avatar: str = attr.ib(default=None)
