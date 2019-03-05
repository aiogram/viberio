from viberio import types
from viberio.api.client import ViberBot
from viberio.dispatcher.events import Event, SkipHandler
from viberio.types import requests, messages
from viberio.types.requests import EventType
from viberio.utils.mixins import DataMixin, ContextInstanceMixin


class Dispatcher(DataMixin, ContextInstanceMixin):
    def __init__(self, viber: ViberBot):
        self.viber: ViberBot = viber

        self.loop = self.viber.loop

        self.handlers = Event()
        self.messages_handler = Event()  # ViberMessageRequest
        self.url_messages_handler = Event()  # URLMessage
        self.location_messages_handler = Event()  # LocationMessage
        self.picture_messages_handler = Event()  # PictureMessage
        self.contact_messages_handler = Event()  # ContactMessage
        self.file_messages_handler = Event()  # FileMessage
        self.text_messages_handler = Event()  # TextMessage
        self.video_messages_handler = Event()  # VideoMessage
        self.sticker_messages_handler = Event()  # StickerMessage
        self.rich_media_messages_handler = Event()  # RichMediaMessage
        self.keyboard_messages_handler = Event()  # KeyboardMessage
        self.failed_handler = Event()  # ViberFailedRequest
        self.conversation_started_handler = Event()  # ViberConversationStartedRequest
        self.delivered_handler = Event()  # ViberDeliveredRequest
        self.seen_handler = Event()  # ViberSeenRequest
        self.subscribed_handler = Event()  # ViberSubscribedRequest
        self.unsubscribed_handler = Event()  # ViberUnsubscribedRequest
        self.request_handler = Event()  # ViberRequest
        self.webhook_handler = Event()  # ViberRequest

        self._register_default_handlers()

    def _register_default_handlers(self):
        self.handlers.subscribe(self._process_event, [])
        self.messages_handler.subscribe(self._process_message, [])

    @staticmethod
    def parse_request(data: dict) -> requests.ViberReqestObject:
        return types.requests.parse_request(data)

    def feed_request(self, request: requests.ViberReqestObject):
        return self.loop.create_task(self.handlers.notify(request))

    async def _process_event(self, viber_request: requests.ViberReqestObject, data: dict):
        data['_request'] = viber_request
        if viber_request.event == EventType.SUBSCRIBED:
            result = await self.subscribed_handler.notify(viber_request, data)
        elif viber_request.event == EventType.UNSUBSCRIBED:
            result = await self.unsubscribed_handler.notify(viber_request, data)
        elif viber_request.event == EventType.WEBHOOK:
            result = await self.webhook_handler.notify(viber_request, data)
        elif viber_request.event == EventType.CONVERSATION_STARTED:
            result = await self.conversation_started_handler.notify(viber_request, data)
        elif viber_request.event == EventType.ACTION:
            result = await self.request_handler.notify(viber_request, data)
        elif viber_request.event == EventType.DELIVERED:
            result = await self.delivered_handler.notify(viber_request, data)
        elif viber_request.event == EventType.FAILED:
            result = await self.failed_handler.notify(viber_request, data)
        elif viber_request.event == EventType.MESSAGE:
            result = await self.messages_handler.notify(viber_request, data)
        elif viber_request.event == EventType.SEEN:
            result = await self.seen_handler.notify(viber_request, data)
        else:
            raise SkipHandler()
        if result:
            return result
        raise SkipHandler()

    async def _process_message(self, message_request: requests.ViberMessageRequest, data: dict):
        if message_request.message.type == messages.MessageType.RICH_MEDIA:
            result = await self.rich_media_messages_handler.notify(message_request, data)
        elif message_request.message.type == messages.MessageType.STICKER:
            result = await self.sticker_messages_handler.notify(message_request, data)
        elif message_request.message.type == messages.MessageType.URL:
            result = await self.url_messages_handler.notify(message_request, data)
        elif message_request.message.type == messages.MessageType.LOCATION:
            result = await self.location_messages_handler.notify(message_request, data)
        elif message_request.message.type == messages.MessageType.CONTACT:
            result = await self.contact_messages_handler.notify(message_request, data)
        elif message_request.message.type == messages.MessageType.FILE:
            result = await self.file_messages_handler.notify(message_request, data)
        elif message_request.message.type == messages.MessageType.TEXT:
            result = await self.text_messages_handler.notify(message_request, data)
        elif message_request.message.type == messages.MessageType.PICTURE:
            result = await self.picture_messages_handler.notify(message_request, data)
        elif message_request.message.type == messages.MessageType.VIDEO:
            result = await self.video_messages_handler.notify(message_request, data)
        elif message_request.message.type == messages.MessageType.KEYBOARD:
            result = await self.keyboard_messages_handler.notify(message_request, data)
        else:
            raise SkipHandler()
        if result:
            return result
        raise SkipHandler()
