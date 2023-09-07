import math
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import datetime
from . import Yfinance as Yf
from functools import reduce


START_DATE = "2019-01-01"


def yesterday_date():
    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    return datetime.datetime.strftime(yesterday, '%Y-%m-%d')


def get_ml_raw_data(stock_symbol):
    data_to_download = [stock_symbol, "BTC-USD", "XLP", "XLF", "XLE", "XLI", "XLK", "XLY",
                        "XLB", "XLU", "QQQ", "IEI", "GLD", "TIP", "RLY"]
    df = Yf.download_stock_and_indices(list_of_symbols=data_to_download,
                                       start_date=START_DATE,
                                       end_date=yesterday_date())

    tickers_data = []
    for ticker, data in df.groupby(level=1, axis=1):
        data.columns = data.columns.droplevel(1)
        data['HLP'] = (data['High'] - data['Low']) / data['Low'] * 100.0
        data['pcth'] = (data['Close'] - data['Open']) / data['Open'] * 100.0

        data = data[['Adj Close', 'HLP', 'pcth']]
        data.columns = [f"{col}_{ticker}" for col in data.columns]
        data = data.reset_index()
        tickers_data.append(data)

    df_final = reduce(lambda left, right: pd.merge(left, right, on='Date'), tickers_data)
    forecast_col = f'Adj Close_{stock_symbol}'
    df_final.dropna(inplace=True)
    forecast_out = int(math.ceil(0.02 * len(df_final)))
    df_final['label'] = df_final[forecast_col].shift(-forecast_out)

    return df_final, forecast_out


def fit_model(stock_symbol):
    df, forecast_out = get_ml_raw_data(stock_symbol)
    X = np.array(df.drop(['label', 'Date'], axis=1))
    X = preprocessing.scale(X)
    X_lately = X[-forecast_out:]
    X = X[:-forecast_out]
    df.dropna(inplace=True)

    y = np.array(df['label'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    clf = LinearRegression()
    clf.fit(X_train, y_train)
    # confidence = clf.score(X_test, y_test)
    forecast_set = clf.predict(X_lately)
    df['Forecast'] = np.nan

    last_date = df.iloc[-1]['Date']
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day

    forecast_data = []
    for i in forecast_set:
        next_date = pd.to_datetime(next_unix, unit='s')
        next_unix += 86400
        forecast_data.append({'Date': next_date, 'Forecast': i})

    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    df = pd.concat([df, pd.DataFrame(forecast_data)], ignore_index=True)

    return df
