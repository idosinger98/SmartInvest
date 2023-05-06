import pytest
from stockAnalysis.thirdPartUtils.Yfinance import get_stock_by_date, BadStockRequestException
from pandas import DataFrame


def test_get_stock_by_date_valid():
    start_date = '2022-01-01'
    end_date = '2022-01-10'
    interval = '1d'
    stock_data = get_stock_by_date('AAPL', start_date, end_date, interval)
    assert isinstance(stock_data, DataFrame)
    assert 'Close' in stock_data
    assert 'Open' in stock_data
    assert 'High' in stock_data
    assert 'Low' in stock_data
    assert 'Volume' in stock_data
    assert len(stock_data) >= 1


def test_get_stock_by_date_invalid_date_format():
    start_date = '01-01-2022'
    end_date = '2022-01-10'
    interval = '1d'
    with pytest.raises(BadStockRequestException):
        get_stock_by_date('AAPL', start_date, end_date, interval)


def test_get_stock_by_date_start_date_greater_than_end_date():
    start_date = '2022-01-10'
    end_date = '2022-01-01'
    interval = '1d'
    with pytest.raises(BadStockRequestException):
        get_stock_by_date('AAPL', start_date, end_date, interval)


def test_get_stock_by_date_stock_symbol_not_found():
    start_date = '2022-01-01'
    end_date = '2022-01-10'
    interval = '1d'
    with pytest.raises(BadStockRequestException):
        get_stock_by_date('INVALID', start_date, end_date, interval)
