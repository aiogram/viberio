import attr

from .base import ViberRequestObject


@attr.s
class ViberRequest(ViberRequestObject):
    event: str = attr.ib()
    # event_type: str = attr.ib()
    timestamp: int = attr.ib()
    message_token: int = attr.ib()
