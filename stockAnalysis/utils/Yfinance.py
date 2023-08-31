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

INDICES = {'^HSI', '^JKSE', '^TWII', '^MERV', '^KLSE', '^JN0U.JO', '^DJI', '^KS11', '^GSPC', '^BUK100P', '^GSPTSE',
           '^NYA', '^NZ50', '^N225', '^BVSP', '^TA125.TA', '399001.SZ', '^IPSA', '^STOXX50E', '^AXJO', '^N100',
           '^GDAXI', '^VIX', '^FCHI', '^FTSE', 'PSEI.PS', '^BSESN', '^MXX', '^RUT', '^XAX', 'IMOEX.ME', '000001.SS',
           '^AORD', '^STI', '^NSEI', '^CASE30', '^IXIC', '^BFX'}

INDICES_RATIOS = {'Open': ['regularMarketOpen', 'This refers to the opening price of the index for the current trading'
                                                ' session. The opening price is the price at which the first trade for'
                                                ' the index occurred at the beginning of the trading day.'],
                  'Previous Close': ['regularMarketPreviousClose', 'This represents the closing price of the index from'
                                                                   ' the previous trading session. The closing price is'
                                                                   ' the last traded price before the trading session'
                                                                   ' ended on the previous day.'],
                  'Volume': ['volume', 'This indicates the total number of shares or contracts that were traded for the'
                                       ' index during the current trading session. Volume provides insight into the'
                                       ' level of market activity and liquidity for the index.'],
                  'Avg. Volume': ['averageVolume', 'This is the average volume of trading activity for the index over a'
                                                   ' specified period, often a certain number of trading days. Average'
                                                   ' volume helps traders and investors gauge the index\'s usual'
                                                   ' trading activity level over time.']}

STOCK_RATIOS = {'Current Ratio': ['currentRatio',
                                  "The current ratio is a financial metric used to evaluate"
                                  " a company's short-term liquidity and ability to cover its"
                                  " short-term liabilities with its short-term assets."],
                'Quick Ratio': ['quickRatio',
                                "The quick ratio, also known as the acid-test ratio, is a financial metric"
                                " used to assess a company's short-term liquidity and its ability to cover"
                                " immediate liabilities without relying on the sale of inventory."],
                'Gross Profit Margin': ['grossMargins',
                                        "Gross Profit Margin is a financial metric used to evaluate a"
                                        " company's profitability and efficiency in generating profit"
                                        " from its core business operations."],
                'Short Ratio': ['shortRatio',
                                "The short ratio, also known as the short interest ratio or days"
                                " to cover ratio, is a financial metric used to assess the level"
                                " of short interest in a particular stock."],
                'Price/Earning to Growth': ['pegRatio',
                                            "The Price/Earnings to Growth ratio, often abbreviated as PEG ratio,"
                                            " is a valuation metric used in finance to assess the relationship"
                                            " between a company's stock price, its earnings per share (EPS),"
                                            " and its expected growth rate."]}


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


def get_stock_fundamentals(symbol):
    try:
        response = yf.Ticker(symbol).info
        handle_response(response)
        symbol_keys = set(response.keys())

        if is_index(symbol):
            ratios_present_in_info = {ratio: key for ratio, (key, _) in INDICES_RATIOS.items() if key in symbol_keys}
        else:
            ratios_present_in_info = {ratio: key for ratio, (key, _) in STOCK_RATIOS.items() if key in symbol_keys}

        return dict(map(lambda item: (item[0], response[item[1]]), ratios_present_in_info.items()))

    except ValueError:
        raise StockNotFoundException()


def is_index(symbol):
    return symbol in INDICES
