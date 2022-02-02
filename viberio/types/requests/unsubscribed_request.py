import attr

from viberio.types.requests import ViberRequestObject


@attr.s
class ViberUnsubscribedRequest(ViberRequestObject):
    user_id: str = attr.ib()
