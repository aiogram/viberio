import attr

from .base import ViberReqestObject


@attr.s
class ViberRequest(ViberReqestObject):
    event: str = attr.ib()
    # event_type: str = attr.ib()
    timestamp: int = attr.ib()
    message_token: int = attr.ib()
