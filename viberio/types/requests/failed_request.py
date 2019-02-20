import attr

from viberio.types.requests.base import ViberReqestObject


@attr.s
class ViberFailedRequest(ViberReqestObject):
    message_token: int = attr.ib()
    user_id: str = attr.ib()
    desc: str = attr.ib()
