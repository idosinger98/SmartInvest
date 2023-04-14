from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import datetime

from .exceptions.StockDataException import StockDataException
from .thirdPartUtils import Finnhub
from http import HTTPStatus

RESOLUTION = 'reso'
FROM = 'from'
TO = 'to'
STOCK_SYMBOL = 'sy'

def search_stock_view(request):
    """
    return stock list end of interval according to D
    it is GET request , need to supply symbol and will SET default value of the rest, or you can supply them
    RESOLUTION - the chart interval(1,15,30,60,D,W,M)
    FROM - START FROM DATE
    TO - END OF CHART DATE
    @param request: http GET request
    """
    try:
        symbol = request.GET.get(STOCK_SYMBOL)
        reso = request.GET.get(RESOLUTION, 'D')
        from_date = request.GET.get(FROM, (datetime.datetime.now() - datetime.timedelta(days=5*365)).strftime('%Y-%m-%d %H:%M:%S'))
        to_date = request.GET.get(TO, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        response = Finnhub.get_stock(symbol, from_date, to_date, reso)[Finnhub.CLOSE_PRICE]
        status_code = HTTPStatus.OK
    except StockDataException as e:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        response = e.message
    except KeyError:
        status_code = HTTPStatus.BAD_REQUEST
        response = "no symbol mentioned"

    return JsonResponse(response,status=status_code,safe=False)
