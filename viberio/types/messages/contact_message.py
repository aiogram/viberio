import attr

from viberio.utils.safe import ensure_cls
from .data_types.contact import Contact
from .message import TypedMessage


@attr.s
class ContactMessage(TypedMessage):
    type: str = attr.ib(default='contact')
    text: str = attr.ib(default=None)
    contact: Contact = attr.ib(default=None, convert=ensure_cls(Contact))
