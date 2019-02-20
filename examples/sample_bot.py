import asyncio

from aiohttp import web

from viberio.api.client import ViberBot
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.webhook import ViberWebhookView
from viberio.types import messages, requests
from viberio.types.configuration import BotConfiguration
from viberio.types.messages.text_message import TextMessage
from viberio.types.requests import ViberMessageRequest, ViberConversationStartedRequest, ViberUnsubscribedRequest, \
    ViberSubscribedRequest


API_TOKEN = 'BOT TOKEN HERE'
WEBHOOK_URL = 'https://example.com'

# logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
loop = asyncio.get_event_loop()
app = web.Application()
bot_config = BotConfiguration(auth_token=API_TOKEN, name='Test bot')
viber = ViberBot(bot_config)
dp = Dispatcher(viber)

ViberWebhookView.bind(dp, app, '/')


@dp.request_handler()
async def webhook(request: ViberMessageRequest, data: dict):
    print('Viber request', request)
    return True


@dp.text_messages_handler(lambda msg: msg.message.text == 'test')
async def test_message(request: requests.ViberMessageRequest, data: dict):
    text = messages.TextMessage(text=f"Hello, {request.sender.name}")
    return await viber.send_message(request.sender.id, text)


@dp.messages_handler()
async def echo(request: ViberMessageRequest, data: dict):
    await viber.send_message(request.sender.id, request.message)
    return True


@dp.conversation_started_handler()
async def start(request: ViberConversationStartedRequest, data: dict):
    await viber.send_message(request.user.id, TextMessage(text='Hello!'))
    return True


@dp.subscribed_handler()
async def subscribed(request: ViberSubscribedRequest, data: dict):
    await viber.send_message(request.user.id, TextMessage(text='Thanks for subscription!'))
    return True


@dp.unsubscribed_handler()
async def unsubscribed(request: ViberUnsubscribedRequest, data: dict):
    # await viber.send_message(request.user_id, TextMessage(text='Bye!'))
    return True


async def set_webhook():
    await asyncio.sleep(1)
    result = await viber.set_webhook(WEBHOOK_URL)


async def on_shutdown(application: web.Application):
    # await viber.unset_webhook()
    await viber.close()


if __name__ == '__main__':
    app.on_shutdown.append(on_shutdown)
    loop.create_task(set_webhook())
    web.run_app(app, host='0.0.0.0', port=8443)
