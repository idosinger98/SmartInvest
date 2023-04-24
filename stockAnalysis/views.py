from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import datetime
import json

from django.views.decorators.csrf import csrf_exempt

from .exceptions.StockDataException import StockDataException
from .thirdPartUtils import Yfinance
from http import HTTPStatus

INTERVAL = 'interval'
FROM = 'from'
TO = 'to'
STOCK_SYMBOL = 'sy'

@csrf_exempt
def search_stock_view(request):
    try:
        symbol = request.GET.get(STOCK_SYMBOL)
        interval = request.GET.get(INTERVAL, '1d')
        from_date = request.GET.get(FROM, (datetime.datetime.now() - datetime.timedelta(days=1*365)).strftime('%Y-%m-%d'))
        to_date = request.GET.get(TO, datetime.datetime.now().strftime('%Y-%m-%d'))
        stock_details = Yfinance.get_stock_by_date(symbol, from_date, to_date, interval)
        status_code = HTTPStatus.OK
    except StockDataException as e:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        response = e.message
        return JsonResponse(response,status=status_code,safe=False)
    except KeyError:
        status_code = HTTPStatus.BAD_REQUEST
        response = "no symbol mentioned"
        return JsonResponse(response,status=status_code,safe=False)

    print(stock_details)
    return JsonResponse(list(stock_details.values()),status=status_code,safe=False)