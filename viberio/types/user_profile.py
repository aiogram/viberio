import attr

from viberio.types.base import ViberBaseObject


@attr.s
class UserProfile(ViberBaseObject):
    id: str = attr.ib()
    name: str = attr.ib()
    avatar: str = attr.ib()
    country: str = attr.ib()
    language: str = attr.ib()
    api_version: int = attr.ib()
