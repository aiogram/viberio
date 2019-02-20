from viberio.api.exceptions import ViberException
from .base import ViberReqestObject
from .conversation_started_request import ViberConversationStartedRequest
from .delivered_request import ViberDeliveredRequest
from .failed_request import ViberFailedRequest
from .message_request import ViberMessageRequest
from .request import ViberRequest
from .seen_request import ViberSeenRequest
from .subscribed_request import ViberSubscribedRequest
from .unsubscribed_request import ViberUnsubscribedRequest


class EventType:
    SUBSCRIBED = 'subscribed'
    UNSUBSCRIBED = 'unsubscribed'
    WEBHOOK = 'webhook'
    CONVERSATION_STARTED = 'conversation_started'
    ACTION = 'action'
    DELIVERED = 'delivered'
    FAILED = 'failed'
    MESSAGE = 'message'
    SEEN = 'seen'


EVENT_TYPE_TO_CLASS = {
    EventType.MESSAGE: ViberMessageRequest,
    EventType.FAILED: ViberFailedRequest,
    EventType.CONVERSATION_STARTED: ViberConversationStartedRequest,
    EventType.DELIVERED: ViberDeliveredRequest,
    EventType.SEEN: ViberSeenRequest,
    EventType.SUBSCRIBED: ViberSubscribedRequest,
    EventType.UNSUBSCRIBED: ViberUnsubscribedRequest,
    EventType.WEBHOOK: ViberRequest
}


def parse_request(request_data: dict) -> ViberReqestObject:
    event = request_data.get('event', None)
    event_object = EVENT_TYPE_TO_CLASS.get(event, None)
    if not event_object:
        raise ViberException(f"Event {event} is not supported", -1, request_data)

    return event_object(**request_data)
