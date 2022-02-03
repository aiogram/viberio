import asyncio

from aiohttp import web

from viberio.api.client import ViberBot
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.webhook import ViberWebhookView
from viberio.types import messages, requests
from viberio.types.configuration import BotConfiguration
from viberio.contrib.fsm_storage.memory import MemoryStorage

from viberio.dispatcher.filters.builtin import StateFilter

API_TOKEN = 'BOT TOKEN HERE'
WEBHOOK_URL = 'https://example.com'

loop = asyncio.get_event_loop()
app = web.Application()
bot_config = BotConfiguration(auth_token=API_TOKEN, name='Test bot')
viber = ViberBot(bot_config)
dp = Dispatcher(viber, MemoryStorage())

ViberWebhookView.bind(dp, app, '/')


async def state_filter(user_id: str, state: str):
    dp_ = Dispatcher.get_current()  # getting Dispatcher instance without using global "dp" variable (for example)
    curr_state = dp_.current_state(user=user_id)
    return await curr_state.get_state() == state


@dp.text_messages_handler(lambda msg: msg.message.text == 'begin')
async def begin_login_flow(request: requests.ViberMessageRequest, data: dict):
    state = dp.current_state(user=request.sender.id)
    await state.set_state('MENU:first_name_input')

    text = messages.TextMessage(text=f"Hello, {request.sender.name}. Provide your first name:")
    return await viber.send_message(request.sender.id, text)


@dp.text_messages_handler(StateFilter('MENU:first_name_input'))
async def process_first_name_from_user(request: requests.ViberMessageRequest, data: dict):
    state = data['state']  # we can access state through data argument
    await state.set_state('MENU:last_name_input')

    async with state.proxy() as data:
        data['first_name'] = request.message.text

    text = messages.TextMessage(text="Provide your last name:")
    return await viber.send_message(request.sender.id, text)


@dp.text_messages_handler(StateFilter('MENU:last_name_input'))
async def process_last_name_from_user(request: requests.ViberMessageRequest, data: dict):
    state = data['state']  # we can access state through data argument

    async with state.proxy() as data:
        first_name = data['first_name']

    text = messages.TextMessage(text=f"Hello, {first_name} {request.message.text}")

    await state.reset_state(with_data=True)  # resets state with all data available
    return await viber.send_message(request.sender.id, text)


async def set_webhook():
    await asyncio.sleep(1)
    await viber.set_webhook(WEBHOOK_URL)


async def on_shutdown(application: web.Application):
    await viber.close()


if __name__ == '__main__':
    app.on_shutdown.append(on_shutdown)
    loop.create_task(set_webhook())
    web.run_app(app, host='0.0.0.0', port=8443)
