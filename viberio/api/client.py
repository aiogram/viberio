from viberio.api.base import BaseViberBot
from viberio.utils.mixins import ContextInstanceMixin


class ApiMethods:
    SET_WEBHOOK = 'set_webhook'
    GET_ACCOUNT_INFO = 'get_account_info'
    SEND_MESSAGE = 'send_message'
    GET_ONLINE = 'get_online'
    GET_USER_DETAILS = 'get_user_details'
    POST = 'post'


class ViberBot(ContextInstanceMixin, BaseViberBot):
    async def set_webhook(self, url, webhook_events=None, is_inline=False):
        payload = {
            'auth_token': self.bot_configuration.auth_token,
            'url': url,
            'is_inline': is_inline
        }
        if webhook_events is not None:
            if not isinstance(webhook_events, list):
                webhook_events = [webhook_events]
            payload['event_types'] = webhook_events

        result = await self.post(ApiMethods.SET_WEBHOOK, payload)
        return result['event_types']

    async def unset_webhook(self):
        return await self.set_webhook('')

    async def send_message(self, to, message, chat_id=None):
        return await self._send_message(
            to,
            self.bot_configuration.name,
            self.bot_configuration.avatar,
            message,
            chat_id
        )

    async def send_messages(self, to, messages, chat_id=None):
        if not isinstance(messages, list):
            messages = [messages]

        send_messages_tokens = []

        for message in messages:
            token = await self.send_message(to, message, chat_id)
            send_messages_tokens.append(token)

        return send_messages_tokens

    async def _send_message(self, to, sender_name, sender_avatar, message, chat_id=None):
        payload = self._prepare_payload(
            message=message,
            receiver=to,
            sender_name=sender_name,
            sender_avatar=sender_avatar,
            chat_id=chat_id
        )
        result = await self.post(ApiMethods.SEND_MESSAGE, payload)
        return result.get('message_token')

    async def get_account_info(self):
        payload = {
            'auth_token': self.bot_configuration.auth_token
        }
        result = await self.post(ApiMethods.GET_ACCOUNT_INFO, payload)
        return result


"""
conversation_started_request
delivered_request
event_types
failed_request
message_request
request
seen_request
subscribed_request
unsubscribed_request

"""
