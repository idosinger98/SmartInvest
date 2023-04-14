import datetime
import finnhub
import json
from stockAnalysis.exceptions.StockDataException import StockDataException

# BASE_URL = "https://finnhub.io/api/v1/"
TOKEN = "cgrd41hr01qs9ra1pu7gcgrd41hr01qs9ra1pu80"
# GET_SYMBOL_URL = BASE_URL + "search?q={}&token=" + TOKEN
# GET_STOCK_URL = BASE_URL + "stock/candle?symbol={0}&resolution={1}&from={2}&to={3}&token=" + TOKEN
AVAILABLE_RESOLUTION = {'1','15','30','60','D','W','M'}
CLOSE_PRICE = 'c'
HIGH_PRICE = 'h'
LOW_PRICE = 'l'
VOLUME = 'v'
TIMESTAMP = 't'

def get_stock(stock_name, start_time, end_time, resolution_candle = 'D'):
    print(stock_name)
    if resolution_candle not in AVAILABLE_RESOLUTION:
        resolution_candle = 'D'
    try:
        start_date_timestamp = __convert_date_to_unix(start_time)
        end_date_timestamp = __convert_date_to_unix(end_time)
        response = finnhub.Client(TOKEN).stock_candles(stock_name,resolution_candle,start_date_timestamp,end_date_timestamp)
        return handle_response(response)
    except ValueError:
        raise StockDataException('date is not match, please make sure the date is in this format: "%Y-%m-%d %H:%M:%S"')
    except (finnhub.FinnhubAPIException, finnhub.FinnhubRequestException) as e:
        raise StockDataException("internal server error")
    except Exception as e:
        raise StockDataException(e.args[0])

def handle_response(response):
    if response['s'] != 'ok':
        raise Exception("symbol not found or there is no data to retrieve")

    response.pop('o')

    return response

def __convert_date_to_unix(date):
    return int(datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timestamp())