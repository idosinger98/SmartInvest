import re
import yfinance as yf
from stockAnalysis.exceptions.BadStockRequestException import BadStockRequestException
from stockAnalysis.exceptions.StockNotFoundException import StockNotFoundException
import datetime


AVAILABLE_INTERVAL = {'1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'}
AVAILABLE_PERIOD = {'1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'}
DATE_PATTERN = re.compile("^(\\d{4})-(\\d{2})-(\\d{2})$")
CLOSE_PRICE = 'Close'
HIGH_PRICE = 'High'
LOW_PRICE = 'Low'
OPEN_PRICE = 'Open'
VOLUME = 'Volume'

INDICES = {'Open': 'regularMarketOpen',
           'Previous Close': 'regularMarketPreviousClose',
           'Volume': 'volume',
           'Avg. Volume': 'averageVolume'}

STOCK_RATIOS = {'Current Ratio': ['currentRatio',
                                  "The current ratio is a financial metric used to evaluate"
                                  " a company's short-term liquidity and ability to cover its"
                                  " short-term liabilities with its short-term assets."],  # 15%
                'Quick Ratio': ['quickRatio',
                                "The quick ratio, also known as the acid-test ratio, is a financial metric"
                                " used to assess a company's short-term liquidity and its ability to cover"
                                " immediate liabilities without relying on the sale of inventory."],  # 10%
                'Gross Profit Margin': ['grossMargins',
                                        "Gross Profit Margin is a financial metric used to evaluate a"
                                        " company's profitability and efficiency in generating profit"
                                        " from its core business operations."],  # 20%
                'Short Ratio': ['shortRatio',
                                "The short ratio, also known as the short interest ratio or days"
                                " to cover ratio, is a financial metric used to assess the level"
                                " of short interest in a particular stock."],  # 5%
                'Price/Earning to Growth': ['pegRatio',
                                            "The Price/Earnings to Growth ratio, often abbreviated as PEG ratio,"
                                            " is a valuation metric used in finance to assess the relationship"
                                            " between a company's stock price, its earnings per share (EPS),"
                                            " and its expected growth rate."]}  # 25%

STOCK_FORMULAS = {'Price-to-Earning (P/E) ratio': ['pegRatio',
                                                   'earningsGrowth',
                                                   "The Price-to-Earnings (P/E) ratio is a financial metric used to"
                                                   " assess the relative valuation of a company's stock by comparing"
                                                   " its market price per share to its earnings per share (EPS)."]}


def get_last_price_stock(stock_name):
    ticker = yf.Ticker(stock_name).history()
    handle_response(ticker)

    return ticker.tail(1)["Close"].iloc[0]


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
        raise StockNotFoundException()


def handle_response(response):
    if len(response) == 0:
        raise StockNotFoundException()

    return response


def __check_date_in_correct_format(date):
    if not DATE_PATTERN.match(date):
        raise BadStockRequestException('date is not match, please make sure the date is in this format: "YYYY-MM-DD"')


def __check_start_date_before_end(start, end):
    if datetime.datetime.strptime(start, '%Y-%m-%d') >= datetime.datetime.strptime(end, '%Y-%m-%d'):
        raise BadStockRequestException('Invalid input - start date cannot be after end date.')


def get_stock_fundamentals(stock_name):
    response = yf.Ticker(stock_name).info

    if stock_name[0] == '^':
        total_ratios = dict(map(lambda item: (item[0], response[item[1]]), INDICES.items()))
    else:
        total_ratios = dict(map(lambda item: (item[0], response[item[1][0]]), STOCK_RATIOS.items()))
        total_ratios.update(dict(map(lambda item: (item[0], response[item[1][0]] * response[item[1][1]]),
                                     STOCK_FORMULAS.items())))

    return total_ratios
