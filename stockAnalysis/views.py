import datetime
import json
import pandas as pd
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .exceptions.ExceptionHandler import handle_exception
from .exceptions.UnsupportedMediaException import UnsupportedMediaException
from .utils import Yfinance
from http import HTTPStatus
from .utils.IndicatorsAlgo import calculate_algorithms
from .utils.StockPrediction import get_ml_prediction
from django.shortcuts import render, redirect
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
from community.views import create_post
from django.contrib import messages
from community.forms import PostForm
from community.models import Post
from django.utils import timezone


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
def my_analysis_page(request):
    profile = Profile.objects.filter(user_id=request.user).first()
    my_analysis = AnalyzedStock.objects.get_user_stocks(analyst_id=profile.user_id)
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
        StockSymbol.objects.get_or_create(symbol=symbol.upper())
        return render(request,
                      'stockAnalysis/graph_page.html',
                      {StockViewParams.STOCK_SYMBOL.value: symbol, StockViewParams.STOCK_DATA.value: response_dict,
                       StockViewParams.INDICATORS.value: get_indicators_dict(), 'fundamentals': fundamentals,
                       'notIndex': not Yfinance.is_index(symbol)})
    except Exception as e:
        error_msg, status_code = handle_exception(e)
        messages.error(request, error_msg)
        return redirect('landing_page')


def compare_stocks(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            symbol = data.get('symbol')
            fundamentals_items = data.get('fundamentalsItems')

            if symbol:
                fundamentals = Yfinance.get_stock_fundamentals(symbol)

                if not fundamentals:
                    return JsonResponse('Stock does not exists!', status=HTTPStatus.INTERNAL_SERVER_ERROR, safe=False)

                is_better = new_stock_is_better(fundamentals, fundamentals_items)

                return JsonResponse({'fundamentals': fundamentals, 'is_better': is_better})

    except Exception as e:
        error_msg, status_code = handle_exception(e)
        return JsonResponse(error_msg, status=status_code, safe=False)


def get_stock_fundamentals_score(fundamentals):
    scaled_data = {key: float(value) * (1 / len(fundamentals)) for key, value in fundamentals.items()}

    return sum(scaled_data.values())


def new_stock_is_better(fundamentals, fundamentals_items):
    return get_stock_fundamentals_score(fundamentals) > get_stock_fundamentals_score(fundamentals_items)


# @csrf_exempt
# @require_POST
# def post_ml_algorithm(request):
#     try:
#         body = json_to_object(request.body)
#         symbol = body[StockViewParams.STOCK_SYMBOL.value]
#         ml_df = fit_model(symbol)
#         adj_close_col = f'Adj Close_{symbol}'
#         result_dict = {}
#
#         for column_name in ['adj_close_col', 'Forecast']:
#             inner_dict = {}
#
#             for index, row in ml_df.iterrows():
#                 if pd.notna(row[column_name]):
#                     inner_dict[str(row['Date']).split(" ")[0]] = row[column_name]
#
#             result_dict[column_name] = inner_dict
#
#     except Exception as e:
#         error_msg, status_code = handle_exception(e)
#         return JsonResponse(error_msg, status=status_code, safe=False)
#
#     result = json.dumps(result_dict)
#
#     return JsonResponse(result, status=HTTPStatus.OK, safe=False)


@csrf_exempt
@require_POST
def post_ml_algorithm(request):
    try:
        body = json_to_object(request.body)
        symbol = body[StockViewParams.STOCK_SYMBOL.value]
        previous_df, predicted_df = get_ml_prediction(symbol)
        result_dict = {}

        for column_name in ['last_original_days_value', 'next_predicted_days_value']:
            inner_dict = {}

            for index, row in ml_df.iterrows():
                if pd.notna(row[column_name]):
                    inner_dict[str(row['Date']).split(" ")[0]] = row[column_name]

            result_dict[column_name] = inner_dict

    except Exception as e:
        error_msg, status_code = handle_exception(e)
        return JsonResponse(error_msg, status=status_code, safe=False)

    result = json.dumps(result_dict)

    return JsonResponse(result, status=HTTPStatus.OK, safe=False)

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
        if type(algos_array) is not list:
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
        stock_symbol_value = request_body['stockSymbolValue']
        if not isinstance(request_body[SaveViewParams.DESCRIPTION.value], str) or \
                not isinstance(request_body[SaveViewParams.PUBLISH.value], bool) or \
                not is_valid_json_chart(chart_json):
            raise ValueError('error occur, chart did not saved')
        stock_analyzed = AnalyzedStock(
            analyst_id=user,
            symbol=StockSymbol.objects.get(symbol=stock_symbol_value.upper()),
            stock_image=chart_json,
            description=request_body[SaveViewParams.DESCRIPTION.value],
            is_public=False)
        stock_analyzed.save()
        if request_body[SaveViewParams.PUBLISH.value]:
            chart_title = request_body[SaveViewParams.TITLE.value]
            if create_post(stock_analyzed, request_body[SaveViewParams.DESCRIPTION.value], chart_title):
                stock_analyzed.is_public = True
                stock_analyzed.save()
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


@login_required
def my_analysis_details_view(request, pk):
    stock_analyzed = AnalyzedStock.objects.filter(id=pk, analyst_id__user_id=request.user).first()
    if stock_analyzed is None:
        return HttpResponse('Error')
    elif stock_analyzed.is_public is False:
        context = {
            'stock_analyzed': stock_analyzed,
            'post_chart': stock_analyzed.stock_image
        }
        return render(request, 'stockAnalysis/my_analysis_details.html', context)
    else:
        post = Post.objects.filter(analysis_id=stock_analyzed).first()
        return redirect('post-details', post_id=post.id)


@login_required
def edit_analysis_details_view(request, pk):
    stock_analyzed = AnalyzedStock.objects.filter(id=pk, analyst_id__user_id=request.user).first()
    if stock_analyzed is None:
        return HttpResponse('Error')

    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post.objects.create(analysis_id=stock_analyzed, description=form.cleaned_data['description'],
                                       title=form.cleaned_data['title'], time=timezone.now())
            post.save()
            stock_analyzed.is_public = True
            stock_analyzed.save()
            return redirect('post-details', post_id=post.id)
        elif not form.cleaned_data.get('is_public', False):
            stock_analyzed.description = form.cleaned_data['description']
            stock_analyzed.save()
            messages.success(request, 'Your analyze has been change.')
        else:
            messages.error(request, 'in case you want to publish your analysis you must fill the title.')

    return redirect('my_analysis_details', pk)


@login_required
def delete_analysis(request, pk):
    stock_analyzed = AnalyzedStock.objects.filter(id=pk).first()
    stock_analyzed.delete()
    return redirect('my-analysis')
