import attr

from viberio.types.requests import ViberReqestObject


@attr.s
class ViberUnsubscribedRequest(ViberReqestObject):
    user_id: str = attr.ib()
