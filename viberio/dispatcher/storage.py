import copy
import typing

from ..utils.deprecated import warn_deprecated as warn
from ..utils.exceptions import FSMStorageWarning


class BaseStorage:
    """
    You are able to save current user's state
    and data for all steps in states-storage
    """

    async def close(self):
        """
        You have to override this method and use when application shutdowns.
        Perhaps you would like to save data and etc.

        :return:
        """
        raise NotImplementedError

    async def wait_closed(self):
        """
        You have to override this method for all asynchronous storages (e.g., Redis).

        :return:
        """
        raise NotImplementedError

    async def get_state(self, *, user: str, default: typing.Optional[str] = None) -> typing.Optional[str]:
        """
        Get current state of user. Return `default` if no record is found.


        :param user:
        :param default:
        :return:
        """
        raise NotImplementedError

    async def get_data(self, *, user: str, default: typing.Optional[typing.Dict] = None) -> typing.Dict:
        """
        Get state-data for user. Return `default` if no data is provided in storage.


        :param user:
        :param default:
        :return:
        """
        raise NotImplementedError

    async def set_state(self, *, user: str, state: typing.Optional[typing.AnyStr] = None):
        """
        Set new state for user


        :param user:
        :param state:
        """
        raise NotImplementedError

    async def set_data(self, *, user: str, data: typing.Dict = None):
        """
        Set data for user


        :param user:
        :param data:
        """
        raise NotImplementedError

    async def update_data(self, *, user: str, data: typing.Dict = None, **kwargs):
        """
        Update data for user in chat

        You can use data parameter or|and kwargs.


        :param data:
        :param user:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    async def reset_data(self, *, user: str):
        """
        Reset data for user in chat.

        :param user:
        :return:
        """
        await self.set_data(user=user, data={})

    async def reset_state(self, *, user: str, with_data: typing.Optional[bool] = True):
        """
        Reset state for user in chat.
        You may desire to use this method when finishing conversations.


        :param user:
        :param with_data:
        :return:
        """
        await self.set_state(user=user, state=None)
        if with_data:
            await self.set_data(user=user, data={})

    async def finish(self, *, user: str):
        """
        Finish conversation for user in chat.

        :param user:
        :return:
        """
        await self.reset_state(user=user, with_data=True)

    @staticmethod
    def resolve_state(value):

        if value is None:
            return

        if isinstance(value, str):
            return value

        return str(value)


class FSMContext:
    def __init__(self, storage, user):
        self.storage: BaseStorage = storage
        self.user = user

    def proxy(self):
        return FSMContextProxy(self)

    async def get_state(self, default: typing.Optional[str] = None) -> typing.Optional[str]:
        return await self.storage.get_state(user=self.user, default=default)

    async def get_data(self, default: typing.Optional[str] = None) -> typing.Dict:
        return await self.storage.get_data(user=self.user, default=default)

    async def update_data(self, data: typing.Dict = None, **kwargs):
        await self.storage.update_data(user=self.user, data=data, **kwargs)

    async def set_state(self, state: typing.Optional[typing.AnyStr] = None):
        await self.storage.set_state(user=self.user, state=state)

    async def set_data(self, data: typing.Dict = None):
        await self.storage.set_data(user=self.user, data=data)

    async def reset_state(self, with_data: typing.Optional[bool] = True):
        await self.storage.reset_state(user=self.user, with_data=with_data)

    async def reset_data(self):
        await self.storage.reset_data(user=self.user)

    async def finish(self):
        await self.storage.finish(user=self.user)


class FSMContextProxy:
    def __init__(self, fsm_context: FSMContext):
        super(FSMContextProxy, self).__init__()
        self.fsm_context = fsm_context
        self._copy = {}
        self._data = {}
        self._state = None
        self._is_dirty = False

        self._closed = True

    async def __aenter__(self):
        await self.load()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.save()
        self._closed = True

    def _check_closed(self):
        if self._closed:
            raise LookupError('Proxy is closed!')

    @classmethod
    async def create(cls, fsm_context: FSMContext):
        """
        :param fsm_context:
        :return:
        """
        proxy = cls(fsm_context)
        await proxy.load()
        return proxy

    async def load(self):
        self._closed = False

        self.clear()
        self._state = await self.fsm_context.get_state()
        self.update(await self.fsm_context.get_data())
        self._copy = copy.deepcopy(self._data)
        self._is_dirty = False

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._check_closed()

        self._state = value
        self._is_dirty = True

    @state.deleter
    def state(self):
        self._check_closed()

        self._state = None
        self._is_dirty = True

    async def save(self, force=False):
        self._check_closed()

        if self._copy != self._data or force:
            await self.fsm_context.set_data(data=self._data)
        if self._is_dirty or force:
            await self.fsm_context.set_state(self.state)
        self._is_dirty = False
        self._copy = copy.deepcopy(self._data)

    def clear(self):
        del self.state
        return self._data.clear()

    def get(self, value, default=None):
        return self._data.get(value, default)

    def setdefault(self, key, default):
        self._check_closed()

        return self._data.setdefault(key, default)

    def update(self, data=None, **kwargs):
        self._check_closed()

        if data is None:
            data = {}
        self._data.update(data, **kwargs)

    def pop(self, key, default=None):
        self._check_closed()

        return self._data.pop(key, default)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def as_dict(self):
        return copy.deepcopy(self._data)

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._check_closed()

        self._data[key] = value

    def __delitem__(self, key):
        self._check_closed()

        del self._data[key]

    def __contains__(self, item):
        return item in self._data

    def __str__(self):
        readable_state = f"'{self.state}'" if self.state else "<default>"
        result = f"{self.__class__.__name__} state = {readable_state}, data = {self._data}"
        if self._closed:
            result += ', closed = True'
        return result


class DisabledStorage(BaseStorage):
    """
    Empty storage. Use it if you don't want to use Finite-State Machine
    """

    async def close(self):
        pass

    async def wait_closed(self):
        pass

    async def get_state(self, *, user: str, default: typing.Optional[str] = None) -> typing.Optional[str]:
        return None

    async def get_data(self, *, user: str, default: typing.Optional[typing.Dict] = None) -> typing.Dict:
        self._warn()
        return {}

    async def set_state(self, *, user: str, state: typing.Optional[typing.AnyStr] = None):
        self._warn()

    async def set_data(self, *, user: str, data: typing.Dict = None):
        self._warn()

    async def update_data(self, *, user: str, data: typing.Dict = None, **kwargs):
        self._warn()

    @staticmethod
    def _warn():
        warn(f"You haven’t set any storage yet so no states and no data will be saved. \n"
             f"You can connect MemoryStorage for debug purposes or non-essential data.",
             FSMStorageWarning, 5)
