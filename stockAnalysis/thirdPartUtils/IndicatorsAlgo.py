import enum
import sys

import pandas as pd
from . import Yfinance as Yf
import numpy as np
from sklearn.linear_model import LinearRegression


RECOMMENDED_WINDOW = 14


class Indicators(enum.Enum):
    RSI = 'rsi_algo'
    MACD = 'macd_algo'
    MTM = 'momentum_algo'
    BOLLINGER_BANDS = 'bollinger_algo'
    LINEAR_REGRESSION = 'linear_reg_algo'
    STOCHASTIC_OSCILLATOR = 'stochastic_algo'
    FORCE = 'force_algo'
    MAD = 'mad_algo'                    # Mean Absolute Deviation
    MA21 = 'ma_golden_death_cross'


def get_indicators_dict():
    dictionary = {}
    for alg in Indicators.__members__:
        dictionary[alg] = "some data on the algorithm"

    return dictionary


def calculate_algorithms(chosen_algos_list, stock_df):
    result = {}
    for alg in chosen_algos_list:
        if alg in Indicators.__members__:
            result[alg] = getattr(sys.modules.get(__name__), Indicators[alg].value)(stock_df).to_json()

    return result


def rsi_algo(stock_df):
    delta = pd.DataFrame(stock_df[Yf.CLOSE_PRICE].diff())
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    avg_gains = gains.rolling(window=RECOMMENDED_WINDOW).mean()
    avg_loss = losses.rolling(window=RECOMMENDED_WINDOW).mean()
    rs = avg_gains/avg_loss
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.rename(columns={Yf.CLOSE_PRICE: Indicators.RSI.name})

    return rsi


def bollinger_algo(stock_df):
    rolling_mean = stock_df[Yf.CLOSE_PRICE].rolling(window=RECOMMENDED_WINDOW).mean()
    bollinger = (stock_df[Yf.CLOSE_PRICE] - rolling_mean)**2
    rolling_std = np.sqrt(bollinger.rolling(window=RECOMMENDED_WINDOW).sum())
    upper_band = rolling_mean + (rolling_std * 2)
    lower_band = rolling_mean - (rolling_std * 2)
    df_result = pd.concat([rolling_mean, upper_band, lower_band], axis=1, keys=['rolling', 'upper band', 'lower band'])

    return df_result


def linear_reg_algo(stock_df):
    y = stock_df['Close'].values
    X = np.arange(len(y)).reshape(-1, 1)

    # Split the data into training and testing sets
    X_train, y_train = X, y
    X_test = X

    # Create the LinearRegression model and fit it to the training data
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)

    # Make predictions for the future time steps
    y_pred = lr_model.predict(X_test)

    # Create a DataFrame containing the predicted prices and the corresponding dates
    prediction_dates = stock_df.index
    prediction_df = pd.DataFrame({'Predicted_Price': y_pred}, index=prediction_dates)

    return prediction_df


def force_algo(stock_df):
    force_index = stock_df[Yf.VOLUME] * (stock_df[Yf.CLOSE_PRICE] - stock_df[Yf.CLOSE_PRICE].shift(1))
    force_index_ema = force_index.ewm(span=14, min_periods=14).mean()
    result_df = pd.concat([force_index, force_index_ema], axis=1, keys=['force index', 'force index ema'])

    return result_df


def macd_algo(stock_df):
    ema12 = stock_df[Yf.CLOSE_PRICE].ewm(span=12, adjust=False).mean()
    ema26 = stock_df[Yf.CLOSE_PRICE].ewm(span=26, adjust=False).mean()
    macd = pd.Series(ema12 - ema26)
    signal = macd.ewm(span=9, adjust=False).mean()
    # histogram = macd - signal
    result_df = pd.concat([macd, signal], axis=1, keys=['MACD', 'Signal'])

    return result_df


def stochastic_algo(stock_df):
    high_prices = stock_df[Yf.HIGH_PRICE].rolling(window=14).max()
    low_prices = stock_df[Yf.LOW_PRICE].rolling(window=14).min()
    k_percent = 100 * (stock_df[Yf.CLOSE_PRICE] - low_prices) / (high_prices - low_prices)
    k_percent_smooth = k_percent.rolling(window=3).mean()
    d_percent = k_percent_smooth.rolling(window=3).mean()
    result_df = pd.concat([k_percent_smooth, d_percent], axis=1, keys=['k percent smooth', 'd percent'])

    return result_df


def mad_algo(stock_df):
    stock_df['MovingAverage'] = stock_df['Close'].rolling(window=10).mean()

    # Calculate the deviation from the moving average
    stock_df['Moving Average Deviation'] = stock_df['Close'] - stock_df['MovingAverage']

    # Create a DataFrame containing only the 'Date' and 'MovingAverageDeviation' columns
    result_df = stock_df[['Moving Average Deviation']].dropna()

    return result_df


def ma_golden_death_cross(stock_df):
    prices = stock_df[Yf.CLOSE_PRICE]
    if len(prices) < 200:
        return None

    ma_21 = prices.rolling(window=21).mean()
    ma_200 = prices.rolling(window=200).mean()
    result_df = pd.concat([ma_21, ma_200], axis=1, keys=['moving average-21', 'moving average-200'])

    return result_df


def momentum_algo(stock_df):
    # Calculate the daily price changes (price differences)
    daily_price_changes = stock_df['Close'].diff()
    # Calculate the Momentum indicator for each day
    result_df = daily_price_changes.rolling(RECOMMENDED_WINDOW).sum()

    # Create a DataFrame containing the Momentum values and the corresponding time index
    result_df = pd.DataFrame({'Momentum': result_df})

    return result_df
