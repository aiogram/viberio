import attr

from viberio.utils.safe import ensure_cls
from viberio.types.user_profile import UserProfile
from .base import ViberRequestObject


@attr.s
class ViberSubscribedRequest(ViberRequestObject):
    user: UserProfile = attr.ib(convert=ensure_cls(UserProfile))
    api_version: str = attr.ib()
