import abc
import inspect


def wrap_async(func):
    async def async_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    if inspect.isawaitable(func) \
            or inspect.iscoroutinefunction(func) \
            or isinstance(func, AbstractFilter):
        return func
    return async_wrapper


class AbstractFilter(abc.ABC):
    """
    Abstract class for custom filters
    """

    @abc.abstractmethod
    async def check(self, event) -> bool:
        """
        Check object
        :param event:
        :return:
        """
        pass

    async def __call__(self, *args) -> bool:
        return await self.check(*args)

    def __invert__(self):
        return NotFilter(self)

    def __and__(self, other):
        if isinstance(self, AndFilter):
            self.append(other)
            return self
        return AndFilter(self, other)

    def __or__(self, other):
        if isinstance(self, OrFilter):
            self.append(other)
            return self
        return OrFilter(self, other)


class Filter(AbstractFilter):
    pass


class _LogicFilter(Filter):
    pass


class NotFilter(_LogicFilter):
    def __init__(self, target):
        self.target = wrap_async(target)

    async def check(self, *args):
        return not bool(await self.target(*args))


class AndFilter(_LogicFilter):

    def __init__(self, *targets):
        self.targets = list(wrap_async(target) for target in targets)

    async def check(self, *args):
        """
        All filters must return a positive result
        :param args:
        :return:
        """
        data = {}
        for target in self.targets:
            result = await target(*args)
            if not result:
                return False
            if isinstance(result, dict):
                data.update(result)
        if not data:
            return True
        return data

    def append(self, target):
        self.targets.append(wrap_async(target))


class OrFilter(_LogicFilter):
    def __init__(self, *targets):
        self.targets = list(wrap_async(target) for target in targets)

    async def check(self, *args):
        """
        One of filters must return a positive result
        :param args:
        :return:
        """
        for target in self.targets:
            result = await target(*args)
            if result:
                if isinstance(result, dict):
                    return result
                return True
        return False

    def append(self, target):
        self.targets.append(wrap_async(target))
