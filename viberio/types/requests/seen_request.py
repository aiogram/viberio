import attr

from viberio.types.requests import ViberRequestObject


@attr.s
class ViberSeenRequest(ViberRequestObject):
    message_token: int = attr.ib()
    user_id: str = attr.ib()
