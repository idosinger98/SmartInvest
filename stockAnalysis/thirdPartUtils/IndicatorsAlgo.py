import enum
import sys
import pandas
import Yfinance as Yf
import numpy as np
from sklearn.linear_model import LinearRegression


class Indicators(enum.Enum):
    RSI = 'rsi_algo'
    MACD = 'macd_algo'
    MTM = 'momentum_algo'
    BOLLINGER_BANDS = 'bollinger_algo'
    LINEAR_REGRESSION = 'linear_reg_algo'
    STOCHASTIC_OSCILLATOR = 'stochastic_algo'
    FORCE = 'force_algo'


def calculate_algorithms(chosen_algos_list, stock_df):
    result = {}
    for alg in chosen_algos_list:
        for indicator in Indicators:
            if indicator.name == alg:
                result[indicator.name] = getattr(sys.modules.get(__name__), indicator.value)(stock_df)
                break

    return result


def rsi_algo(stock_df):
    delta = pandas.DataFrame(stock_df[Yf.CLOSE_PRICE].diff())
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    avg_gains = gains.rolling(window=14).mean()
    avg_loss = losses.rolling(window=14).mean()

    rs = avg_gains/avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def bollinger_algo(stock_df):
    rolling_mean = stock_df[Yf.CLOSE_PRICE].rolling(window=14).mean()
    bolinger = (stock_df[Yf.CLOSE_PRICE] - rolling_mean)**2
    rolling_std = np.sqrt(bolinger.rolling(window=14).sum())
    upper_band = rolling_mean + (rolling_std * 2)
    lower_band = rolling_mean - (rolling_std * 2)

    return rolling_mean, upper_band, lower_band


def linear_reg_algo(stock_df):
    stock_df.dropna(inplace=True)
    stock_df.index = pandas.to_datetime(stock_df.index, format='%Y-%m-%d')
    x = np.array(range(1, len(stock_df) + 1)).reshape((-1, 1))
    y = stock_df[Yf.CLOSE_PRICE].values
    model = LinearRegression()
    model.fit(x, y)
    future_dates = np.array(range(len(stock_df) + 1, len(stock_df) + 11)).reshape((-1, 1))
    future_prices = model.predict(future_dates)

    return future_prices


def force_index(df):
    df = df.copy()
    df['force_index'] = df['Volume'] * (df['Close'] - df['Close'].shift(1))
    df['force_index_ema'] = df['force_index'].ewm(span=14, min_periods=14).mean()

    return df
