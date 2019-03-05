import attr

from viberio.utils.mixins import DataMixin, ContextInstanceMixin


@attr.s
class ViberBaseObject(DataMixin, ContextInstanceMixin):
    pass
