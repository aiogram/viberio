import attr

from .base import ViberRequestObject


@attr.s
class ViberDeliveredRequest(ViberRequestObject):
    message_token: int = attr.ib()
    user_id: str = attr.ib(default=None)
    chat_id: str = attr.ib(default=None)
