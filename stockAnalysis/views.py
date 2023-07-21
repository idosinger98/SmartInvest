from django.http import JsonResponse
import datetime
from django.views.decorators.csrf import csrf_exempt
from .exceptions import ExceptionHandler as eh
from .exceptions.UnsupportedMediaException import UnsupportedMediaException
from .thirdPartUtils import Yfinance
from http import HTTPStatus
import json
from .thirdPartUtils.IndicatorsAlgo import calculate_algorithms
from stockAnalysis.exceptions.StockNotFoundException import StockNotFoundException


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
        response_dict = handle_post_search_stock(request, stock_details)
        response_dict.update({'stock': stock_details.to_json()})
        print(response_dict)
        response = JsonResponse(response_dict, status=HTTPStatus.OK, safe=False)
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


def handle_post_search_stock(request, stock_df):
    dictionary = {}
    if request.method == 'POST':
        if request.content_type != 'application/json':
            raise UnsupportedMediaException()
        try:
            algos_array = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            raise ValueError("post body not contain json str")

        if type(algos_array) != list:
            raise ValueError("JSON content is not a list type")

        dictionary.update(calculate_algorithms(algos_array, stock_df))

    return dictionary

# now we used to_json() on data frame to return the stock data frame as json to client.
# TODO:  need to choose dataformat to return or if json so need to check if we serialized
#  manually be more efficient(to_json returns maps from date to value for each value
#  (returns same date a lot of time))
