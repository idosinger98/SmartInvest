import django.utils.datastructures

from .UnsupportedMediaException import UnsupportedMediaException
from .StockNotFoundException import StockNotFoundException
from .BadStockRequestException import BadStockRequestException
from http import HTTPStatus


EXCEPTION_HANDLER = {
    BadStockRequestException: HTTPStatus.BAD_REQUEST,
    StockNotFoundException: HTTPStatus.NOT_FOUND,
    UnsupportedMediaException: HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
    django.utils.datastructures.MultiValueDictKeyError: HTTPStatus.BAD_REQUEST,
    ValueError: HTTPStatus.BAD_REQUEST,
    KeyError: HTTPStatus.BAD_REQUEST
}
