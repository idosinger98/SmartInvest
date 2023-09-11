# import math
# import numpy as np
# import pandas as pd
# from sklearn import preprocessing
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# import datetime
# from . import Yfinance as Yf
# from functools import reduce
#
#
# START_DATE = "2019-01-01"
#
#
# def yesterday_date():
#     yesterday = datetime.datetime.now() - datetime.timedelta(1)
#     return datetime.datetime.strftime(yesterday, '%Y-%m-%d')
#
#
# def get_ml_raw_data(stock_symbol):
#     data_to_download = [stock_symbol, "BTC-USD", "XLP", "XLF", "XLE", "XLI", "XLK", "XLY",
#                         "XLB", "XLU", "QQQ", "IEI", "GLD", "TIP", "RLY"]
#     df = Yf.download_stock_and_indices(list_of_symbols=data_to_download,
#                                        start_date=START_DATE,
#                                        end_date=yesterday_date())
#
#     tickers_data = []
#     for ticker, data in df.groupby(level=1, axis=1):
#         data.columns = data.columns.droplevel(1)
#         data['HLP'] = (data['High'] - data['Low']) / data['Low'] * 100.0
#         data['pcth'] = (data['Close'] - data['Open']) / data['Open'] * 100.0
#
#         data = data[['Adj Close', 'HLP', 'pcth']]
#         data.columns = [f"{col}_{ticker}" for col in data.columns]
#         data = data.reset_index()
#         tickers_data.append(data)
#
#     df_final = reduce(lambda left, right: pd.merge(left, right, on='Date'), tickers_data)
#     forecast_col = f'Adj Close_{stock_symbol}'
#     df_final.dropna(inplace=True)
#     forecast_out = int(math.ceil(0.02 * len(df_final)))
#     df_final['label'] = df_final[forecast_col].shift(-forecast_out)
#
#     return df_final, forecast_out
#
#
# def fit_model(stock_symbol):
#     df, forecast_out = get_ml_raw_data(stock_symbol)
#     X = np.array(df.drop(['label', 'Date'], axis=1))
#     X = preprocessing.scale(X)
#     X_lately = X[-forecast_out:]
#     X = X[:-forecast_out]
#     df.dropna(inplace=True)
#
#     y = np.array(df['label'])
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
#     clf = LinearRegression()
#     clf.fit(X_train, y_train)
#     # confidence = clf.score(X_test, y_test)
#     forecast_set = clf.predict(X_lately)
#     df['Forecast'] = np.nan
#
#     last_date = df.iloc[-1]['Date']
#     last_unix = last_date.timestamp()
#     one_day = 86400
#     next_unix = last_unix + one_day
#
#     forecast_data = []
#     for i in forecast_set:
#         next_date = pd.to_datetime(next_unix, unit='s')
#         next_unix += 86400
#         forecast_data.append({'Date': next_date, 'Forecast': i})
#
#     df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
#     df = pd.concat([df, pd.DataFrame(forecast_data)], ignore_index=True)
#
#     return df

import os
import pandas as pd
import numpy as np
import math
import datetime as dt
from . import Yfinance as Yf

from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score, r2_score
from sklearn.metrics import mean_poisson_deviance, mean_gamma_deviance, accuracy_score
from sklearn.preprocessing import MinMaxScaler

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import LSTM, GRU

import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from datetime import datetime

# from itertools import cycle
# import plotly.graph_objects as go
# import plotly.express as px
# from plotly.subplots import make_subplots


def get_ml_prediction(stock_symbol):
    # df = get_stock_data(stock_symbol)
    df = Yf.download_stock(list_of_symbols=stock_symbol)
    df = df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close',
                                    'Adj Close': 'adj_close', 'Volume': 'volume'})
    df['date'] = df.index
    # ---------------------------------------------------------------------------------------------------------
    # monthvise = df.groupby(df['date'].dt.strftime('%B'))[['open', 'close']].mean()
    # new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    #              'September', 'October', 'November', 'December']
    # monthvise = monthvise.reindex(new_order, axis=0)
    # ---------------------------------------------------------------------------------------------------------
    df.groupby(df['date'].dt.strftime('%B'))['low'].min()
    # monthvise_high = df.groupby(df['date'].dt.strftime('%B'))['high'].max()
    # monthvise_high = monthvise_high.reindex(new_order, axis=0)

    # monthvise_low = df.groupby(df['date'].dt.strftime('%B'))['low'].min()
    # monthvise_low = monthvise_low.reindex(new_order, axis=0)
    # ---------------------------------------------------------------------------------------------------------
    # names = cycle(['Stock Open Price', 'Stock Close Price', 'Stock High Price', 'Stock Low Price'])
    # ---------------------------------------------------------------------------------------------------------
    closedf = df[['date', 'close']]
    # ---------------------------------------------------------------------------------------------------------
    closedf = closedf[closedf['date'] > '2020-08-16']
    # close_stock = closedf.copy()
    # ---------------------------------------------------------------------------------------------------------
    del closedf['date']
    scaler = MinMaxScaler(feature_range=(0, 1))
    closedf = scaler.fit_transform(np.array(closedf).reshape(-1, 1))
    # ---------------------------------------------------------------------------------------------------------
    training_size = int(len(closedf) * 0.60)
    # test_size = len(closedf) - training_size
    train_data, test_data = closedf[0:training_size, :], closedf[training_size:len(closedf), :1]
    # ---------------------------------------------------------------------------------------------------------
    time_step = 15
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, y_test = create_dataset(test_data, time_step)
    # ---------------------------------------------------------------------------------------------------------
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
    # ---------------------------------------------------------------------------------------------------------
    tf.keras.backend.clear_session()
    model = Sequential()
    model.add(GRU(32, return_sequences=True, input_shape=(time_step, 1)))
    model.add(GRU(32, return_sequences=True))
    model.add(GRU(32))
    model.add(Dropout(0.20))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    # ---------------------------------------------------------------------------------------------------------
    history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=200, batch_size=32, verbose=1)
    # ---------------------------------------------------------------------------------------------------------
    # loss = history.history['loss']
    # val_loss = history.history['val_loss']
    # ---------------------------------------------------------------------------------------------------------
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)
    # train_predict.shape, test_predict.shape
    # ---------------------------------------------------------------------------------------------------------
    train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)
    # original_ytrain = scaler.inverse_transform(y_train.reshape(-1, 1))
    # original_ytest = scaler.inverse_transform(y_test.reshape(-1, 1))
    # ---------------------------------------------------------------------------------------------------------
    look_back = time_step
    trainPredictPlot = np.empty_like(closedf)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(train_predict) + look_back, :] = train_predict

    # shift test predictions for plotting
    testPredictPlot = np.empty_like(closedf)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(train_predict) + (look_back * 2) + 1:len(closedf) - 1, :] = test_predict

    # names = cycle(['Original close price', 'Train predicted close price', 'Test predicted close price'])
    # ---------------------------------------------------------------------------------------------------------
    x_input = test_data[len(test_data) - time_step:].reshape(1, -1)
    temp_input = list(x_input)
    temp_input = temp_input[0].tolist()

    from numpy import array

    lst_output = []
    n_steps = time_step
    i = 0
    pred_days = 30
    while (i < pred_days):

        if (len(temp_input) > time_step):

            x_input = np.array(temp_input[1:])
            # print("{} day input {}".format(i,x_input))
            x_input = x_input.reshape(1, -1)
            x_input = x_input.reshape((1, n_steps, 1))

            yhat = model.predict(x_input, verbose=0)
            # print("{} day output {}".format(i,yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input = temp_input[1:]
            # print(temp_input)

            lst_output.extend(yhat.tolist())
            i = i + 1

        else:

            x_input = x_input.reshape((1, n_steps, 1))
            yhat = model.predict(x_input, verbose=0)
            temp_input.extend(yhat[0].tolist())

            lst_output.extend(yhat.tolist())
            i = i + 1

    print("Output of predicted next days: ", len(lst_output))
    # ---------------------------------------------------------------------------------------------------------
    last_days = np.arange(1, time_step + 1)
    # day_pred = np.arange(time_step + 1, time_step + pred_days + 1)
    # ---------------------------------------------------------------------------------------------------------
    temp_mat = np.empty((len(last_days) + pred_days + 1, 1))
    temp_mat[:] = np.nan
    temp_mat = temp_mat.reshape(1, -1).tolist()[0]

    last_original_days_value = temp_mat
    next_predicted_days_value = temp_mat

    last_original_days_value[0:time_step + 1] = \
    scaler.inverse_transform(closedf[len(closedf) - time_step:]).reshape(1, -1).tolist()[0]
    next_predicted_days_value[time_step + 1:] = \
    scaler.inverse_transform(np.array(lst_output).reshape(-1, 1)).reshape(1, -1).tolist()[0]

    new_pred_plot = pd.DataFrame({
        'last_original_days_value': last_original_days_value,
        'next_predicted_days_value': next_predicted_days_value
    })
    return new_pred_plot
    # ---------------------------------------------------------------------------------------------------------


def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)
# def get_stock_data(stock_symbol):
#     return Yf.download_stock(list_of_symbols=stock_symbol)
#
# def create_date_column(df):

