import attr

from viberio.types.base import ViberBaseObject


@attr.s
class Contact(ViberBaseObject):
    name: str = attr.ib(default=None)
    phone_number: str = attr.ib(default=None)
    avatar: str = attr.ib(default=None)
