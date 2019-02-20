from viberio.types.messages.message import TypedMessage
from .contact_message import ContactMessage
from .file_message import FileMessage
from .keyboard_message import KeyboardMessage
from .location_message import LocationMessage
from .picture_message import PictureMessage
from .rich_media_message import RichMediaMessage
from .sticker_message import StickerMessage
from .text_message import TextMessage
from .url_message import URLMessage
from .video_message import VideoMessage


class MessageType(object):
    RICH_MEDIA = 'rich_media'
    STICKER = 'sticker'
    URL = 'url'
    LOCATION = 'location'
    CONTACT = 'contact'
    FILE = 'file'
    TEXT = 'text'
    PICTURE = 'picture'
    VIDEO = 'video'
    KEYBOARD = 'keyboard'


MESSAGE_TYPE_TO_CLASS = {
    MessageType.URL: URLMessage,
    MessageType.LOCATION: LocationMessage,
    MessageType.PICTURE: PictureMessage,
    MessageType.CONTACT: ContactMessage,
    MessageType.FILE: FileMessage,
    MessageType.TEXT: TextMessage,
    MessageType.VIDEO: VideoMessage,
    MessageType.STICKER: StickerMessage,
    MessageType.RICH_MEDIA: RichMediaMessage,
    MessageType.KEYBOARD: KeyboardMessage
}


def parse_message(message_data: dict) -> TypedMessage:
    message_type = message_data.get('type')
    if not message_type:
        raise ValueError('This message is not typed!')
    message_object = MESSAGE_TYPE_TO_CLASS.get(message_type)
    if not message_object:
        raise ValueError(f"Message type '{message_type}' is not supported")
    return message_object(**message_data)
