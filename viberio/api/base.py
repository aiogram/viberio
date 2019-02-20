import asyncio
import hashlib
import hmac
import ssl

import aiohttp
import attr
import certifi

from viberio.api.exceptions import ViberApiException
from viberio.types.configuration import BotConfiguration
from viberio.types.errors import ViberBaseError
from viberio.types.messages.picture_message import PictureMessage
from viberio.types.messages.sticker_message import StickerMessage

VIBER_BOT_API_URL = "https://chatapi.viber.com/pa"
VIBER_BOT_USER_AGENT = "ViberBot-Python/0.0.1"


class BaseViberBot:
    api_url = VIBER_BOT_API_URL
    user_agent = VIBER_BOT_USER_AGENT

    def __init__(self, config: BotConfiguration, connections_limit=None, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self.bot_configuration = config

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = aiohttp.TCPConnector(limit=connections_limit, ssl_context=ssl_context,
                                         loop=self.loop)

        self.session = aiohttp.ClientSession(connector=connector, loop=self.loop)

    async def close(self):
        await self.session.close()

    def url(self, uri: str) -> str:
        return self.api_url + '/' + uri

    async def post(self, uri, payload):
        headers = {
            'User-Agent': self.user_agent
        }
        url = self.url(uri)
        async with self.session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                raise ViberApiException(response, await response.text(), payload)
            result = await response.json()
            ViberBaseError.check(result)
            return result

    def verify_signature(self, request_data, signature):
        return signature == self._calculate_message_signature(request_data)

    def _calculate_message_signature(self, message):
        return hmac.new(
            bytes(self.bot_configuration.auth_token.encode('ascii')),
            msg=message,
            digestmod=hashlib.sha256) \
            .hexdigest()

    def _cleanup_data(self, message: dict) -> dict:
        # return {k: self._cleanup_data(v) if isinstance(v, dict) else v for k, v in message.items() if v is not None}
        return {k: v for k, v in message.items() if v is not None}

    def _prepare_payload(self, message, sender_name, sender_avatar, sender=None, receiver=None, chat_id=None):
        payload = attr.asdict(message)
        if isinstance(message, PictureMessage):
            payload.pop('file_name', None)
        elif isinstance(message, StickerMessage):
            payload.pop('media', None)

        payload.update({
            'auth_token': self.bot_configuration.auth_token,
            'from': sender,
            'receiver': receiver,
            'sender': {
                'name': sender_name,
                'avatar': sender_avatar
            },
            "chat_id": chat_id
        })

        return self._cleanup_data(payload)
