import attr

from viberio.utils.safe import ensure_cls
from .data_types.location import Location
from .message import TypedMessage

@attr.s
class LocationMessage(TypedMessage):
    type: str = attr.ib(default='location')
    location: Location = attr.ib(default=None, convert=ensure_cls(Location))
