import attr

from .base import ViberReqestObject


@attr.s
class ViberDeliveredRequest(ViberReqestObject):
    message_token: int = attr.ib()
    user_id: str = attr.ib(default=None)
    chat_id: str = attr.ib(default=None)
