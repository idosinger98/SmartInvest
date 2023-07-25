from django.http import JsonResponse
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .exceptions import ExceptionHandler as eh
from .exceptions.UnsupportedMediaException import UnsupportedMediaException
from .thirdPartUtils import Yfinance
from http import HTTPStatus
import json
from .thirdPartUtils.IndicatorsAlgo import calculate_algorithms
from django.shortcuts import render
from .exceptions.StockNotFoundException import StockNotFoundException
from .thirdPartUtils.IndicatorsAlgo import get_indicators_dict
from pandas import DataFrame


INTERVAL = 'interval'
FROM = 'from'
TO = 'to'
STOCK_SYMBOL = 'sy'


def get_biggest_indices(request):
    stocks = ['^IXIC', '^DJI', '^GSPC']
    dictionary = {}

    for stock in stocks:
        try:
            price = Yfinance.get_last_price_stock(stock)
            dictionary[stock] = str(price)
        except StockNotFoundException:
            dictionary[stock] = '-'

    return JsonResponse(dictionary)


@csrf_exempt
def search_stock_view(request):
    try:
        symbol = request.GET[STOCK_SYMBOL]
        interval = request.GET.get(INTERVAL, '1d')
        from_date = request.GET.get(
            FROM,
            (datetime.datetime.now() - datetime.timedelta(days=1*365)).strftime('%Y-%m-%d')
        )
        to_date = request.GET.get(TO, datetime.datetime.now().strftime('%Y-%m-%d'))
        stock_details = Yfinance.get_stock_by_date(symbol, from_date, to_date, interval)
        response_dict = {'stock': stock_details.to_json()}
        response = render(request,
                          'stockAnalysis/graph_page.html',
                          {'symbol': symbol, 'stock_data': response_dict,
                           'indicators': get_indicators_dict()})
        # response = JsonResponse(response_dict, status=HTTPStatus.OK, safe=False)
    except Exception as e:
        error_msg, status_code = handle_exception(e)
        return JsonResponse(error_msg, status=status_code, safe=False)

    return response


def handle_exception(exception):
    status_code = eh.EXCEPTION_HANDLER.get(type(exception), HTTPStatus.INTERNAL_SERVER_ERROR)
    error_msg = exception.args[0]
    if isinstance(exception, KeyError):
        error_msg = 'no symbol mentioned'

    if status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        error_msg = "EXCEPTION NOT HANDLE " + exception.args[0]

    return error_msg, status_code


@csrf_exempt
@require_POST
def post_calculate_algorithms(request):
    dictionary = {}
    try:
        if request.content_type != 'application/json':
            raise UnsupportedMediaException()
        try:
            request_dict = json.loads(request.body)
            algos_array = request_dict['algorithms']
            stock_df = DataFrame(request_dict['stock'])
        except json.decoder.JSONDecodeError:
            raise ValueError("post body not contain json str")

        if type(algos_array) != list:
            raise ValueError("JSON content is not a list type")
    except Exception as e:
        error_msg, status_code = handle_exception(e)
        return JsonResponse(error_msg, status=status_code, safe=False)

    dictionary.update(calculate_algorithms(algos_array, stock_df))

    return JsonResponse(dictionary, status=HTTPStatus.OK, safe=False)
