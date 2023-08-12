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


def handle_exception(exception):
    status_code = EXCEPTION_HANDLER.get(type(exception), HTTPStatus.INTERNAL_SERVER_ERROR)
    error_msg = exception.args[0]
    if isinstance(exception, KeyError):
        error_msg = 'JSON keys not compatible'

    if status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        error_msg = "EXCEPTION NOT HANDLE " + exception.args[0]

    return error_msg, status_code
