import logging

from viberio.types.messages import TypedMessage
from viberio.types.requests import ViberReqestObject, ViberUnsubscribedRequest, ViberSubscribedRequest, \
    ViberDeliveredRequest, ViberConversationStartedRequest, ViberFailedRequest, ViberMessageRequest, ViberRequest
from viberio.types.requests.seen_request import ViberSeenRequest
from viberio.types.user_profile import UserProfile


class ViberLoggingFilter(logging.Filter):
    def __init__(self, name='', prefix='viber'):
        super(ViberLoggingFilter, self).__init__(name)
        self.prefix = prefix

    def make_prefix(self, prefix, iterable):
        """
        Add prefix to the label

        :param prefix:
        :param iterable:
        :return:
        """
        if not prefix:
            yield from iterable

        for key, value in iterable:
            yield f"{prefix}_{key}", value

    def filter(self, record: logging.Filter):
        request = ViberReqestObject.get_current()

        if request:
            for key, value in self.make_prefix(self.prefix, self.process_request(request)):
                setattr(record, key, value)

        return True

    def process_request(self, event: ViberReqestObject):
        yield 'event_type', event.event

        if isinstance(event, ViberMessageRequest):
            yield from self.process_user(event.sender)
            yield from self.process_message(event.message)

        elif isinstance(event, ViberFailedRequest):
            yield 'user_id', event.user_id

        elif isinstance(event, ViberConversationStartedRequest):
            yield from self.process_user(event.user)

        elif isinstance(event, ViberDeliveredRequest):
            yield 'user_id', event.user_id

        elif isinstance(event, ViberSeenRequest):
            yield 'user_id', event.user_id

        elif isinstance(event, ViberSubscribedRequest):
            yield from self.process_user(event.user)

        elif isinstance(event, ViberUnsubscribedRequest):
            yield 'user_id', event.user_id
        #
        # elif isinstance(event, ViberRequest):
        #     pass

    def process_user(self, user: UserProfile):
        if not user:
            return

        yield 'user_id', user.id
        if user.name:
            yield 'user_name', user.name
        elif user.country:
            yield 'user_country', user.country
        elif user.language:
            yield 'user_language', user.language

    def process_message(self, message: TypedMessage):
        yield 'message_type', message.type

        # if isinstance(message, URLMessage):
        #     pass
        #
        # elif isinstance(message, LocationMessage):
        #     pass
        #
        # elif isinstance(message, PictureMessage):
        #     pass
        #
        # elif isinstance(message, ContactMessage):
        #     pass
        #
        # elif isinstance(message, FileMessage):
        #     pass
        #
        # elif isinstance(message, TextMessage):
        #     pass
        #
        # elif isinstance(message, VideoMessage):
        #     pass
        #
        # elif isinstance(message, StickerMessage):
        #     pass
        #
        # elif isinstance(message, RichMediaMessage):
        #     pass
        #
        # elif isinstance(message, KeyboardMessage):
        #     pass
