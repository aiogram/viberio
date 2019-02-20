import functools
import inspect

from dateutil import parser


def ensure_cls(klass):
    def converter(val):
        if val is None:
            return
        if isinstance(val, dict):
            return klass(**val)
        if isinstance(val, list):
            return [converter(v) for v in val]
        if not isinstance(val, klass):
            return klass(val)
        return val

    return converter


def ensure_factory(func):
    def converter(val):
        if val is None:
            return
        elif isinstance(val, dict):
            return func(val)
        if isinstance(val, list):
            return [converter(v) for v in val]
        return val

    return converter


def parse_date(val):
    if val:
        return parser.parse(val)


def safe_kwargs(func_or_class):
    spec = inspect.getfullargspec(func_or_class)
    all_args = spec.args

    @functools.wraps(func_or_class)
    def wrap(*args, **kwargs):
        accepted_kwargs = {k: v for k, v in kwargs.items() if k in all_args}
        return func_or_class(*args, **accepted_kwargs)

    return wrap
