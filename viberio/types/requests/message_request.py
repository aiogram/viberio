import attr

from viberio.utils.safe import ensure_cls, ensure_factory
from viberio.types.messages.message import TypedMessage
from viberio.types.messages.message_type import parse_message
from viberio.types.user_profile import UserProfile
from .base import ViberReqestObject


@attr.s
class ViberMessageRequest(ViberReqestObject):
    message: TypedMessage = attr.ib(convert=ensure_factory(parse_message))
    sender: UserProfile = attr.ib(convert=ensure_cls(UserProfile))
    file_name: str
    chat_id: str = attr.ib(default=None)
    reply_type: str = attr.ib(default=None)
    silent: str = attr.ib(default=None)
