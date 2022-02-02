import copy
import typing

from ...dispatcher.storage import BaseStorage


class MemoryStorage(BaseStorage):
    """
    In-memory based states storage.

    This type of storage is not recommended for usage in bots, because you will lost all states after restarting.
    """

    async def wait_closed(self):
        pass

    async def close(self):
        self.data.clear()

    def __init__(self):
        self.data = {}

    def check_address(self, user: str):
        if user not in self.data:
            self.data[user] = {'state': None, 'data': {}}

        return user

    async def get_state(self, *, user: str, default: typing.Optional[str] = None) -> typing.Optional[str]:
        self.check_address(user)

        return self.data[user].get("state", self.resolve_state(default))

    async def get_data(self, *, user: str, default: typing.Optional[str] = None) -> typing.Dict:
        self.check_address(user)

        return copy.deepcopy(self.data[user]['data'])

    async def update_data(self, *, user: str, data: typing.Dict = None, **kwargs):
        self.check_address(user)

        if data is None:
            data = {}
        self.data[user]['data'].update(data, **kwargs)

    async def set_state(self, *, user: str, state: typing.AnyStr = None):
        self.check_address(user)

        self.data[user]['state'] = self.resolve_state(state)

    async def set_data(self, *, user: str, data: typing.Dict = None):
        self.check_address(user)

        self.data[user]['data'] = copy.deepcopy(data)
        self._cleanup(user)

    async def reset_state(self, *, user: str, with_data: typing.Optional[bool] = True):
        await self.set_state(user=user, state=None)
        if with_data:
            await self.set_data(user=user, data={})
        self._cleanup(user)

    def _cleanup(self, user: str):
        if self.data[user] == {'state': None, 'data': {}, 'bucket': {}}:
            del self.data[user]
