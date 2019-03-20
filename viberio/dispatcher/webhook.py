import contextvars
import logging

from aiohttp import web

from viberio.api.client import ViberBot
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types.requests import ViberReqestObject

VIBER_DISPATCHER = '#viber-dispatcher'

log = logging.getLogger(__name__)


class ViberWebhookView(web.View):
    _event = contextvars.ContextVar('viber_event')

    def get_current_event(self):
        return self._event.get(None)

    @property
    def viber(self) -> ViberBot:
        return self.request.app[VIBER_DISPATCHER].viber

    @property
    def dispatcher(self) -> Dispatcher:
        return self.request.app[VIBER_DISPATCHER]

    def get_signature(self):
        return self.request.headers.get('X-Viber-Content-Signature') or self.request.query.get('sig')

    async def verify_data(self):
        signature = self.get_signature()
        text = await self.request.text()
        if not self.viber.verify_signature(text.encode(), signature):
            log.warning(f"Received message with invalid signature.")
            raise web.HTTPBadRequest()

    async def post(self):
        await self.verify_data()
        data = await self.request.json()

        try:
            request_object = self.dispatcher.parse_request(data)
            ViberReqestObject.set_current(request_object)

        except TypeError as e:
            log.exception(f"Failed to parse input message: {data} with error: {e}")

        else:
            log.debug(f"Received {request_object.event} event: {request_object}")
            try:
                await self.dispatcher.feed_request(request_object)
            except Exception as e:
                log.exception(f"Cause exception while process {request_object}: {e}")

        finally:
            return web.Response(status=200)

    @classmethod
    def bind(cls, dispatcher: Dispatcher, app: web.Application, path: str = '/', name='viber-webhook'):
        app.router.add_route('*', path, cls, name=name)
        app[VIBER_DISPATCHER] = dispatcher
