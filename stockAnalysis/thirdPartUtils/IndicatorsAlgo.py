import enum
import sys
from pandas import DataFrame
import Yfinance as Yf

class Indicators(enum.Enum):
    RSI = 'rsi_algo'
    MACD = 'macd_algo'
    MTM = 'momentum_algo'
    BOLLINGER_BANDS = 'bollinger_algo'
    LINEAR_REGRESSION = 'linear_reg_algo'
    STOCHASTIC_OSCILLATOR = 'stochastic_algo'
    FORCE = 'force_algo'


def calculate_algorithms(chosen_algos_list,stock_df):
    result = {}
    for alg in chosen_algos_list:
        for indicator in Indicators:
            if indicator.name == alg:
                result[indicator.name] = getattr(sys.modules.get(__name__),indicator.value)(stock_df)
                break

    return result

def rsi_algo(stock_df):
    delta = DataFrame(stock_df[Yf.CLOSE_PRICE].diff())
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    avg_gains = gains.rolling(window=14).mean()
    avg_loss = losses.rolling(window=14).mean()

    rs = avg_gains/avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

