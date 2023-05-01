import re
import yfinance as yf
from stockAnalysis.exceptions.StockDataException import StockDataException
import datetime


AVAILABLE_INTERVAL = {'1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'}
AVAILABLE_PERIOD = {'1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'}
DATE_PATTERN = re.compile("^(\\d{4})-(\\d{2})-(\\d{2})$")
CLOSE_PRICE = 'Close'
HIGH_PRICE = 'High'
LOW_PRICE = 'Low'
OPEN_PRICE = 'Open'
VOLUME = 'Volume'


def get_stock_by_date(stock_name, start_date, end_date, interval):
    if interval not in AVAILABLE_INTERVAL:
        interval = '1d'

    __check_date_in_correct_format(start_date)
    __check_date_in_correct_format(end_date)
    __check_start_date_before_end(start_date, end_date)
    try:
        response = yf.Ticker(stock_name).history(interval=interval, start=start_date, end=end_date)
        return handle_response(response)
    except ValueError:
        raise StockDataException('symbol not found')
    except Exception as e:
        raise StockDataException(e.args[0])


def handle_response(response):
    if len(response) == 0:
        raise StockDataException('can not find symbol / there was no trading in this date range')

    return response


def __check_date_in_correct_format(date):
    if not DATE_PATTERN.match(date):
        raise StockDataException('date is not match, please make sure the date is in this format: "YYYY-MM-DD"')


def __check_start_date_before_end(start, end):
    if datetime.datetime.strptime(start, '%Y-%m-%d') >= datetime.datetime.strptime(end, '%Y-%m-%d'):
        raise StockDataException('Invalid input - start date cannot be after end date.')
