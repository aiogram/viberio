import attr

from viberio.utils.mixins import DataMixin, ContextInstanceMixin


@attr.s
class ViberBaseObject(DataMixin, ContextInstanceMixin):
    pass

    @property
    def bot(self):
        from ..api.client import ViberBot

        return ViberBot.get_current()
