import attr

from .message import TypedMessage
from viberio.types.base import ViberBaseObject


@attr.s
class ContentButtons(ViberBaseObject):
    Columns: int = attr.ib(default=None)
    Rows: int = attr.ib(default=None)
    ActionType: str = attr.ib(default=None)
    ActionBody: str = attr.ib(default=None)
    Text: str = attr.ib(default=None)
    TextSize: str = attr.ib(default=None)
    TextVAlign: str = attr.ib(default=None)
    TextHAlign: str = attr.ib(default=None)
    Image: str = attr.ib(default=None)


@attr.s
class RichMedia(ViberBaseObject):
    Type: str = attr.ib(default='rich_media')
    BgColor: str = attr.ib(default=None)
    ButtonsGroupColumns: int = attr.ib(default=None)
    ButtonsGroupRows: int = attr.ib(default=None)
    Buttons: ContentButtons = attr.ib(default=None)


@attr.s
class ContentMessage(TypedMessage):
    type: str = attr.ib(default='rich_media')
    rich_media: RichMedia = attr.ib(default=None)
    min_api_version: RichMedia = attr.ib(default=2)
