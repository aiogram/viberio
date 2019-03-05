import re
from re import Pattern

import validators

from viberio.dispatcher.filters.filters import Filter
from viberio.types.messages import TextMessage
from viberio.types.requests import ViberMessageRequest


class Text(Filter):
    def __init__(self, eq=None, starts=None, ends=None, contains=None, case_insensitive=True):
        self.eq = eq
        self.starts = starts
        self.ends = ends
        self.contains = contains
        self.case_insensitive = case_insensitive

        check = sum(map(bool, (eq, contains, starts, ends)))
        if check > 1:
            args = "' and '".join([arg[0] for arg in [('eq', eq),
                                                      ('contains', contains),
                                                      ('startswith', starts),
                                                      ('ends', ends)
                                                      ] if arg[1]])
            raise ValueError(f"Arguments '{args}' cannot be used together.")
        elif check == 0:
            raise ValueError(f"No one mode is specified!")

    async def check(self, event) -> bool:
        if isinstance(event, ViberMessageRequest):
            message = event.message
            if isinstance(message, TextMessage):
                return self.check_text(message.text)
        return False

    def check_text(self, text: str) -> bool:
        if self.eq:
            return self.eq == text
        elif self.starts:
            return text.startswith(self.starts)
        elif self.ends:
            return text.endswith(self.ends)
        elif self.contains:
            return self.contains in text
        return False


class Regexp(Filter):
    def __init__(self, pattern):
        if not isinstance(pattern, Pattern):
            pattern = re.compile(pattern, flags=re.IGNORECASE | re.MULTILINE)
        self.pattern = pattern

    async def check(self, event) -> bool:
        if isinstance(event, ViberMessageRequest):
            message = event.message
            if isinstance(message, TextMessage):
                return self.check_text(message.text)

        return False

    def check_text(self, text: str):
        match = self.pattern.search(text)
        if match is not None:
            return {'regexp': match}

        return False


class Email(Filter):
    def __init__(self, whitelist=None):
        if whitelist is None:
            whitelist = []
        self.whitelist = whitelist

    async def check(self, event) -> bool:
        if isinstance(event, ViberMessageRequest):
            message = event.message
            if isinstance(message, TextMessage):
                return self.check_text(message.text)

        return False

    def check_text(self, text):
        if validators.email(text, whitelist=self.whitelist or None):
            return True
        return False


class Url(Filter):
    def __init__(self, public=False):
        self.public = public

    async def check(self, event) -> bool:
        if isinstance(event, ViberMessageRequest):
            message = event.message
            if isinstance(message, TextMessage):
                return self.check_text(message.text)

        return False

    def check_text(self, text):
        if validators.url(text, public=self.public):
            return True
        return False
