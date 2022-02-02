import attr

from viberio.types.requests.base import ViberRequestObject


@attr.s
class ViberFailedRequest(ViberRequestObject):
    message_token: int = attr.ib()
    user_id: str = attr.ib()
    desc: str = attr.ib()
