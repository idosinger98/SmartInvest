import pytest
import stockAnalysis.thirdPartUtils.IndicatorsAlgo as algos
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

@pytest.fixture
def sample_df():
    data = {"Open":{"1648785600000":172.9821241694,"1649044800000":173.5188920982,"1649131200000":176.4312464982,"1649217600000":171.3221871912,"1649304000000":170.1294054439,"1649390400000":170.7456835967,"1649649600000":167.6941675201,"1649736000000":167.0083304288,"1649822400000":166.3821070002,"1649908800000":169.5926630087,"1650254400000":162.9329956542,"1650340800000":164.0263848509,"1650427200000":167.7438545675,"1650513600000":167.8929507273,"1650600000000":165.4577208466,"1650859200000":160.1498491913},
            "High":{"1648785600000":173.8270121909,"1649044800000":177.4152873022,"1649131200000":177.2264326144,"1649217600000":172.5845445185,"1649304000000":172.3161556471,"1649390400000":170.7456835967,"1649649600000":168.0122328446,"1649736000000":168.847182199,"1649822400000":170.0101234722,"1649908800000":170.238758348,"1650254400000":165.5968666036,"1650340800000":166.8095285078,"1650427200000":167.8631423354,"1650513600000":170.4971701434,"1650600000000":166.8592194542,"1650859200000":162.1875086348},
            "Low":{"1648785600000":170.9047121797,"1649044800000":173.3896699965,"1649131200000":173.3697898094,"1649217600000":169.105618706,"1649304000000":168.8272957161,"1649390400000":168.1812163744,"1649649600000":164.5034889463,"1649736000000":165.636634764,"1649822400000":165.7658450114,"1649908800000":164.046259321,"1650254400000":162.5851121902,"1650340800000":162.9230677828,"1650427200000":165.0998825219,"1650513600000":164.9110145408,"1650600000000":160.527579232,"1650859200000":157.5058772788},
            "Close":{"1648785600000":173.2604370117,"1649044800000":177.3655853271,"1649131200000":174.0059356689,"1649217600000":170.7953796387,"1649304000000":171.1035003662,"1649390400000":169.0658569336,"1649649600000":164.7519836426,"1649736000000":166.6504974365,"1649822400000":169.3739776611,"1649908800000":164.2947540283,"1650254400000":164.0760803223,"1650340800000":166.3920440674,"1650427200000":166.2230682373,"1650513600000":165.4179382324,"1650600000000":160.815826416,"1650859200000":161.8992614746},
            "Volume":{"1648785600000":78751300,"1649044800000":76468400,"1649131200000":73401800,"1649217600000":89058800,"1649304000000":77594700,"1649390400000":76575500,"1649649600000":72246700,"1649736000000":79265200,"1649822400000":70618900,"1649908800000":75329400,"1650254400000":69023900,"1650340800000":67723800,"1650427200000":67929800,"1650513600000":87227800,"1650600000000":84882400,"1650859200000":96046400},
            }
    return pd.DataFrame(data)

def test_rsi_algo(sample_df):
    expected_result = pd.DataFrame({"RSI":{"1648785600000":np.nan, "1649044800000":np.nan, "1649131200000":np.nan,"1649217600000":np.nan,
                                           "1649304000000":np.nan,"1649390400000":np.nan,"1649649600000":np.nan,
                                           "1649736000000":np.nan,"1649822400000":np.nan,"1649908800000":np.nan,
                                           "1650254400000":np.nan,"1650340800000":np.nan,"1650427200000":np.nan,
                                           "1650513600000":37.1623653582,"1650600000000":32.2963725764,"1650859200000":25.9281635932}
                                    })
    rsi = algos.rsi_algo(sample_df)
    pd.testing.assert_frame_equal(rsi,expected_result)


def test_macd_algo(sample_df):
    expected_result = pd.DataFrame({"MACD":{"1648785600000":0.0,"1649044800000":0.3274762189,"1649131200000":0.3123077428,"1649217600000":0.0407518148,
                                            "1649304000000":-0.1478906556,"1649390400000":-0.4565491537,"1649649600000":-1.0372994173,
                                            "1649736000000":-1.3290337153,"1649822400000":-1.3251971079,"1649908800000":-1.7122694903,
                                            "1650254400000":-2.0134623421,"1650340800000":-2.0417449633,"1650427200000":-2.0541155165,
                                            "1650513600000":-2.1046257166,"1650600000000":-2.4873349274,"1650859200000":-2.6724047612},
                                    "Signal":{"1648785600000":0.0,"1649044800000":0.0654952438,"1649131200000":0.1148577436,"1649217600000":0.1000365578,
                                              "1649304000000":0.0504511151,"1649390400000":-0.0509489386,"1649649600000":-0.2482190344,
                                              "1649736000000":-0.4643819706,"1649822400000":-0.636544998,"1649908800000":-0.8516898965,
                                              "1650254400000":-1.0840443856,"1650340800000":-1.2755845011,"1650427200000":-1.4312907042,
                                              "1650513600000":-1.5659577067,"1650600000000":-1.7502331508,"1650859200000":-1.9346674729}
                                    })
    macd = algos.macd_algo(sample_df)
    pd.testing.assert_frame_equal(macd, expected_result)


def test_force_algo(sample_df):
    expected_result = pd.DataFrame({"force index":{"1648785600000":np.nan,"1649044800000":313914123.4413345456,"1649131200000":-246604332.2812646627,
                                      "1649217600000":-285928267.3823753595,"1649304000000":23908535.4141429029,"1649390400000":-156033564.6730607152,
                                      "1649649600000":-311663109.4928892255,"1649736000000":150486075.5762406886,"1649822400000":192329177.6330066621,
                                      "1649908800000":-382614868.7246460319,"1650254400000":-15093712.015573686,"1650340800000":156845865.4804047942,
                                      "1650427200000":-11478494.3435276393,"1650513600000":-70229719.0414168835,"1650600000000":-390638296.0443910956,
                                      "1650859200000":104060037.0123193115},
                       "force index ema":{"1648785600000":np.nan,"1649044800000":np.nan,"1649131200000":np.nan,"1649217600000":np.nan,"1649304000000":np.nan,
                                          "1649390400000":np.nan,"1649649600000":np.nan,"1649736000000":np.nan,"1649822400000":np.nan,"1649908800000":np.nan,
                                          "1650254400000":np.nan,"1650340800000":np.nan,"1650427200000":np.nan,"1650513600000":np.nan,
                                          "1650600000000":-93712230.9892849624,"1650859200000":-63852226.9089002162}})

    force = algos.force_algo(sample_df)
    pd.testing.assert_frame_equal(force, expected_result)


def test_bollinger_algo(sample_df):
    expected_result = pd.DataFrame({"rolling":{"1648785600000":np.nan,"1649044800000":np.nan,"1649131200000":np.nan,"1649217600000":np.nan,
                                         "1649304000000":np.nan,"1649390400000":np.nan,"1649649600000":np.nan,"1649736000000":np.nan,
                                         "1649822400000":np.nan,"1649908800000":np.nan,"1650254400000":np.nan,"1650340800000":np.nan,
                                         "1650427200000":np.nan,"1650513600000":168.7697884696,"1650600000000":167.8808877127,"1650859200000":166.7761502947},
                                    "upper band":{"1648785600000":np.nan,"1649044800000":np.nan,"1649131200000":np.nan,"1649217600000":np.nan,
                                         "1649304000000":np.nan,"1649390400000":np.nan,"1649649600000":np.nan,"1649736000000":np.nan,
                                         "1649822400000":np.nan,"1649908800000":np.nan,"1650254400000":np.nan,"1650340800000":np.nan,
                                         "1650427200000":np.nan,"1650513600000":np.nan,"1650600000000":np.nan,"1650859200000":np.nan},
                                    "lower band":{"1648785600000":np.nan,"1649044800000":np.nan,"1649131200000":np.nan,"1649217600000":np.nan,
                                         "1649304000000":np.nan,"1649390400000":np.nan,"1649649600000":np.nan,"1649736000000":np.nan,
                                         "1649822400000":np.nan,"1649908800000":np.nan,"1650254400000":np.nan,"1650340800000":np.nan,
                                         "1650427200000":np.nan,"1650513600000":np.nan,"1650600000000":np.nan,"1650859200000":np.nan}
                                    })
    bollinger = algos.bollinger_algo(sample_df)
    pd.testing.assert_frame_equal(bollinger, expected_result)


def test_stochastic_algo(sample_df):
    expected_result = pd.DataFrame({"k percent smooth":{"1648785600000":np.nan,"1649044800000":np.nan,"1649131200000":np.nan,
                                                         "1649217600000":np.nan,"1649304000000":np.nan,"1649390400000":np.nan,
                                                         "1649649600000":np.nan,"1649736000000":np.nan,"1649822400000":np.nan,
                                                         "1649908800000":np.nan,"1650254400000":np.nan,"1650340800000":np.nan,
                                                         "1650427200000":np.nan,"1650513600000":np.nan,"1650600000000":np.nan,
                                                         "1650859200000":14.3622713053},
                                     "d percent":{"1648785600000":np.nan,"1649044800000":np.nan,"1649131200000":np.nan,
                                                  "1649217600000":np.nan,"1649304000000":np.nan,"1649390400000":np.nan,
                                                  "1649649600000":np.nan,"1649736000000":np.nan,"1649822400000":np.nan,
                                                  "1649908800000":np.nan,"1650254400000":np.nan,"1650340800000":np.nan,
                                                  "1650427200000":np.nan,"1650513600000":np.nan,"1650600000000":np.nan,
                                                  "1650859200000":np.nan}})
    stochastic = algos.stochastic_algo(sample_df)
    pd.testing.assert_frame_equal(stochastic, expected_result)

def test_linear_reg_algo(sample_df):
    # Call the function to get the predicted DataFrame
    prediction_df = algos.linear_reg_algo(sample_df)

    # Assert the DataFrame contains the required columns
    assert 'Predicted_Price' in prediction_df.columns

    # Assert the length of the DataFrame is equal to the input DataFrame
    assert len(prediction_df) == len(sample_df)

    # Assert the predicted prices are of numeric type (float or int)
    assert prediction_df['Predicted_Price'].dtype in (np.float64, np.int64)

    # Check the predicted prices against a custom linear regression calculation
    X = np.arange(len(sample_df['Close'])).reshape(-1, 1)
    y = sample_df['Close'].values

    lr_model = LinearRegression()
    lr_model.fit(X, y)
    y_pred_custom = lr_model.predict(X)

    np.testing.assert_array_almost_equal(prediction_df['Predicted_Price'].values, y_pred_custom)



def test_calculate_algos(sample_df):
    result = algos.calculate_algorithms(['RSI','MACD', 'asdas'], sample_df)
    assert 'RSI' in result
    assert 'MACD' in result
    assert len(result.keys()) == 2

def test_mad_algo(sample_df):
    # Call the function to get the DataFrame with moving average deviation
    result_df = algos.mad_algo(sample_df)

    # Assert the DataFrame contains the required columns
    assert 'Moving Average Deviation' in result_df.columns

    # Assert the length of the DataFrame is less than or equal to the input DataFrame
    assert len(result_df) <= len(sample_df)

    # Assert the moving average deviation values are of numeric type (float or int)
    assert result_df['Moving Average Deviation'].dtype in (np.float64, np.int64)

    # Check the moving average deviation calculation against a custom calculation
    moving_average = sample_df['Close'].rolling(window=10).mean()
    moving_average_deviation_custom = sample_df['Close'] - moving_average

    np.testing.assert_array_almost_equal(
        result_df['Moving Average Deviation'].values,
        moving_average_deviation_custom.dropna().values)


def test_momentum_algo(sample_df):
    # Call the function to get the DataFrame with momentum values
    result_df = algos.momentum_algo(sample_df)

    # Assert the DataFrame contains the required column
    assert 'Momentum' in result_df.columns

    # Assert the length of the DataFrame is less than or equal to the input DataFrame
    assert len(result_df) <= len(sample_df)

    # Assert the momentum values are of numeric type (float or int)
    assert result_df['Momentum'].dtype in (np.float64, np.int64)
