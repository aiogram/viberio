import attr

from viberio.utils.safe import ensure_cls
from viberio.types.user_profile import UserProfile
from .base import ViberRequestObject


@attr.s
class ViberConversationStartedRequest(ViberRequestObject):
    message_token: int = attr.ib()
    type: str = attr.ib()
    user: UserProfile = attr.ib(convert=ensure_cls(UserProfile))
    subscribed: str = attr.ib()
    context: str = attr.ib(default=None)
    api_version: str = attr.ib(default=None)
