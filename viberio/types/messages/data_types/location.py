import attr

from viberio.types.base import ViberBaseObject


@attr.s
class Location(ViberBaseObject):
    lat: float = attr.ib()
    lon: float = attr.ib()

    @lat.validator
    def check_lat(self, attribute, value):
        return LocationConsts.MIN_LATITUDE <= value <= LocationConsts.MAX_LATITUDE

    @lon.validator
    def check_lon(self, attribute, value):
        return LocationConsts.MIN_LONGITUDE <= value <= LocationConsts.MAX_LONGITUDE


class LocationConsts(object):
    MAX_LONGITUDE = 180
    MIN_LONGITUDE = -180
    MAX_LATITUDE = 90
    MIN_LATITUDE = -90
