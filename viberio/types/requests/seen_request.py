import attr

from viberio.types.requests import ViberReqestObject


@attr.s
class ViberSeenRequest(ViberReqestObject):
    message_token: int = attr.ib()
    user_id: str = attr.ib()
