import datetime
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .exceptions.ExceptionHandler import handle_exception
from .exceptions.UnsupportedMediaException import UnsupportedMediaException
from .utils import Yfinance
from http import HTTPStatus
from .utils.IndicatorsAlgo import calculate_algorithms
from django.shortcuts import render
from .exceptions.StockNotFoundException import StockNotFoundException
from .utils.IndicatorsAlgo import get_indicators_dict
from pandas import DataFrame
from .models import StockSymbol, AnalyzedStock
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .utils.ViewsParametersEnums import SearchStockViewParameters as StockViewParams
from .utils.ViewsParametersEnums import IndicatorsViewParameters as IndicatorViewsParams
from .utils.ViewsParametersEnums import SaveStockViewParameters as SaveViewParams
from .utils.ViewsParametersEnums import ChartDetails
from utils.Constants import RequestContentType as ReqType


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


@login_required
def my_analysis_page(request, analyst_id):
    my_analysis = AnalyzedStock.objects.get_user_stocks(analyst_id=analyst_id)
    context = {'analysis': my_analysis}
    return render(request, 'stockAnalysis/my-analysis.html', context)


@csrf_exempt
def search_stock_view(request):
    try:
        symbol = request.GET[StockViewParams.STOCK_SYMBOL.value]
        interval = request.GET.get(StockViewParams.INTERVAL.value, '1d')
        from_date = request.GET.get(
            StockViewParams.FROM.value,
            (datetime.datetime.now() - datetime.timedelta(days=1*365)).strftime('%Y-%m-%d')
        )
        to_date = request.GET.get(StockViewParams.TO, datetime.datetime.now().strftime('%Y-%m-%d'))
        stock_details = Yfinance.get_stock_by_date(symbol, from_date, to_date, interval)
        response_dict = {StockViewParams.STOCK.value: stock_details.to_json()}
        fundamentals = Yfinance.get_stock_fundamentals(symbol)
        StockSymbol.objects.aget_or_create(symbol=symbol)

        return render(request,
                      'stockAnalysis/graph_page.html',
                      {StockViewParams.STOCK_SYMBOL.value: symbol, StockViewParams.STOCK_DATA.value: response_dict,
                       StockViewParams.INDICATORS.value: get_indicators_dict(), 'fundamentals': fundamentals})
    # , 'fundamentals': fundamentals
    except Exception as e:
        error_msg, status_code = handle_exception(e)
        return JsonResponse(error_msg, status=status_code, safe=False)


# def search_stock_wrapper(request):
#     from landingPage.views import home
#     response = search_stock_view(request=request)
#     if response.status_code != 200:
#         return home(request=request, return_after_wrong_symbol=True)
#     else:
#         return response


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
        if request.content_type != ReqType.JSON.value:
            raise UnsupportedMediaException()

        request_dict = json_to_object(request.body)
        algos_array = request_dict[IndicatorViewsParams.INDICATORS.value]
        stock_df = DataFrame(request_dict[IndicatorViewsParams.STOCK.value])
        if type(algos_array) != list:
            raise ValueError("JSON content is not a list type")

        dictionary.update(calculate_algorithms(algos_array, stock_df))
    except Exception as e:
        error_msg, status_code = handle_exception(e)
        return JsonResponse(error_msg, status=status_code, safe=False)

    return JsonResponse(dictionary, status=HTTPStatus.OK, safe=False)


@login_required
@csrf_exempt
@require_POST
def save_stock_analysis(request):
    try:
        user = Profile.objects.get(user_id=request.user)
        request_body = json_to_object(request.body)
        chart_json = request_body[SaveViewParams.CHART.value]
        if not isinstance(request_body[SaveViewParams.DESCRIPTION.value], bool) or \
                not isinstance(request_body[SaveViewParams.PUBLISH.value], bool) or \
                not is_valid_json_chart(chart_json):
            raise ValueError('error occur, chart did not saved')

        stock_analyzed = AnalyzedStock(
            analyst_id=user,
            stock_image=chart_json,
            description=request_body[SaveViewParams.DESCRIPTION.value],
            is_public=False)
        stock_analyzed.save()
        # if request_body[SaveViewParams.PUBLISH]:
        #     chart_title = request_body[SaveViewParams.TITLE.value]
        # # call community view of post
        #     stock_analyzed.is_public = True
        #     stock_analyzed.save()
    except Exception as e:
        error_msg, status_code = handle_exception(e)
        return HttpResponse(
            error_msg,
            content_type=ReqType.PLAIN_TEXT.value,
            status=status_code
        )

    return HttpResponse(
        'GREAT, YOUR ANALYZE SAVED AND READY IN YOUR PRIVATE AREA',
        content_type=ReqType.PLAIN_TEXT.value
    )


def json_to_object(json_data):
    try:
        request_dict = json.loads(json_data)
    except json.decoder.JSONDecodeError:
        raise ValueError("post body not contain json str")

    return request_dict


def is_valid_json_chart(json_chart):
    try:
        chart = json.loads(json_chart)
        for param in ChartDetails:
            if param.value not in chart:
                return False
    except json.JSONDecodeError:
        return False

    return True
