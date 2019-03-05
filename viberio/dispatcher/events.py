from __future__ import annotations

import functools
import inspect
import typing

import attr

from viberio.dispatcher.filters.filters import wrap_async


class SkipHandler(Exception):
    pass


class CancelEvent(Exception):
    pass


class DataDict(dict):
    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        del self[item]


class Event:
    def __init__(self):
        self._handlers = []
        self._middlewares = []

    def subscribe(self, callback, filters):
        handler = EventHandler(callback, filters)
        self._handlers.append(handler)
        return handler

    def middleware(self, _func_or_none=None):
        def wrap(func):
            self._middlewares.append(func)
            return func

        if callable(_func_or_none):
            return wrap(_func_or_none)
        return wrap

    async def notify(self, event, data=None):
        if data is None:
            data = DataDict()
        elif not isinstance(data, DataDict):
            data = DataDict(data)

        results = []
        for handler in self._handlers:  # type: EventHandler
            try:
                check = await handler.check(event)
                data.update(check)
                result = await self.call_handler(handler, event, data)

            except SkipHandler:
                continue

            except CancelEvent:
                break

            else:
                if result:
                    results.append(result)
                break

        return results

    async def call_handler(self, handler: EventHandler, event, data):
        handler = handler.run
        for m in reversed(self._middlewares):
            handler = functools.partial(m, handler)
        return await handler(event, data)

    # def handler(self, *filters):
    #     def decorator(callback):
    #         self.register_event_handler(callback, *filters)
    #         return callback
    #
    #     return decorator

    def __call__(self, *args, **kwargs):
        if kwargs:
            raise TypeError('kwargs based filters is not supported yet.')

        def decorator(callback):
            self.subscribe(callback, args)
            return callback

        return decorator


@attr.s
class EventHandler:
    callback: callable = attr.ib()
    filters: typing.Tuple[typing.Union[callable]] = attr.ib()
    spec: inspect.FullArgSpec = attr.ib(init=False)

    # def __attrs_post_init__(self):
    #     self.spec = inspect.getfullargspec(self.callback)

    async def check(self, event):
        data = DataDict()
        for filter_ in self.filters:

            check = await wrap_async(filter_)(event)

            if not check:
                raise SkipHandler()

            elif isinstance(check, dict):
                data.update(check)

        return data

    async def run(self, event, data):
        return await self.callback(event, data)
