import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
from alpha import power,rank,ts_argmax,ts_std
from sklearn.feature_selection import mutual_info_regression
import shap


class PreProcessing:
    def __init__(self):
        pass
    def in_processing(self,df):
        """
        Process the input data by dropping the first two rows, converting relevant columns to numeric,
        setting the index to 'Date'.

        Parameters:
        df : pandas DataFrame
            The input data.

        Returns:
        The processed DataFrame.
        """
        df.drop([0,1],inplace=True)
        df['Date'] = df['Price']
        df.drop(columns=['Price'],inplace=True)
        df.set_index('Date',inplace=True)
        df['High'] = pd.to_numeric(df['High'], errors='coerce')
        df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        df['Open'] = pd.to_numeric(df['Open'], errors='coerce')

        return df
    def alpha054(self,o, h, l, c):
        """-(low - close) * power(open, 5) / ((low - high) * power(close, 5))"""
        return (l.sub(c).mul(o.pow(5)).mul(-1)
            .div(l.sub(h).replace(0, -0.0001).mul(c ** 5)))
    def atr(self,df,timeperiod):
        df.ta.atr(length=timeperiod,append=True,prefix='feature_')
    def alpha041(self,h, l, vwap):
        """power(high * low, 0.5 - vwap"""
        return (power(h.mul(l), 0.5)
            .sub(vwap))
    def bb(self,df,length,std):
        df.ta.bbands(length=length,std=std,append=True,prefix='feature_')
    def alpha001(self,c, r):
        """(rank(ts_argmax(power(((returns < 0)
        ? ts_std(returns, 20)
        : close), 2.), 5)) -0.5)"""
        close = c.copy(deep=True)
        return_ = r.copy(deep=True)
        close.loc[return_ < 0] = ts_std(return_, 20)  
        return (rank(ts_argmax(power(close, 2), 5)).mul(-.5))
    def add_ema_sma(self,df:pd.DataFrame):
        """
        Adds the following indicators to the input DataFrame:

        - EMA (lengths 10 and 20)
        - SMA (lengths 10 and 20)

        Parameters:
        df : pandas DataFrame
            The input data.

        Returns:
        The processed DataFrame with added indicators.

        Raises:
        ValueError
            If the input is not a DataFrame.
        """
        try:
            df.ta.ema(length=10, append=True,prefix='feature_')
            df.ta.ema(length=20,append=True,prefix='feature_')
            df.ta.sma(length=10, append=True,prefix='feature_')
            df.ta.sma(length=20,append=True,prefix='feature_')
            return df
        except ValueError:
            print('make sure you pass a DataFrame') 
    def gann_high_low1(self,df, HPeriod=15, LPeriod=21):
        """
        Calculates the Gann High-Low indicator.

        Parameters:
        df : pandas DataFrame
            The input data. Must contain the 'High', 'Low', and 'Close' columns.
        HPeriod : int, optional
            The length of the short Simple Moving Average (SMA) used in the calculation of the Gann
            High-Low indicator. Default is 15.
        LPeriod : int, optional
            The length of the long SMA used in the calculation of the Gann High-Low indicator. Default
            is 21.

        Returns:
        A DataFrame with the Gann High-Low indicator added as a new column.

        Notes:
        The Gann High-Low indicator is a technical analysis indicator that helps identify trend changes
        in a security's price. It is calculated as the shorter of the two SMAs, or the longer of the two
        SMAs, depending on whether the security is in an uptrend or a downtrend.
        """
        sma_1 = df['High'].rolling(window=HPeriod).mean()
        sma_2 = df['Low'].rolling(window=LPeriod).mean()
        # Calculate HLd
        HLd = np.where(df['Close'] > sma_1.shift(1), 1, 
                   np.where(df['Close'] < sma_2.shift(1), -1, 0))
        # Calculate HLv
        HLv = np.where(HLd != 0, HLd, 0)
        # Calculate HiLo
        HiLo = np.where(HLv == -1, sma_1, sma_2)
        df['feature_gann_hiLo'] = HiLo

        return df
    def add_return(self,df):
        df.ta.percent_return(cumulative=True,append=True)

def plot_mi_scores(scores):
    scores = scores.sort_values(ascending=True)
    width = np.arange(len(scores))
    ticks = list(scores.index)
    plt.barh(width, scores)
    plt.yticks(width, ticks)
    plt.title("Mutual Information Scores")

def make_mi_scores(df):
    X = df.copy()
    y = X.pop("cumpctret_1")

    discrete_features = X.dtypes == int
    
    mi_scores = mutual_info_regression(X, y, discrete_features=discrete_features)
    mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)
    mi_scores = mi_scores.sort_values(ascending=False)
    return mi_scores


def shap_values(model,x):
    X100 = shap.utils.sample(x, 100)
    explainer = shap.Explainer(model.predict, X100)
    shap_values = explainer(x)
    shap.plots.waterfall(shap_values[1000])
    return shap_values

def information_cofe(df):
    fwd_corr = df.drop(['cumpctret_1'], axis=1).corrwith(df.cumpctret_1, method='spearman')
    top50 = fwd_corr.abs().index
    fwd_corr.loc[top50].sort_values().plot.barh(figsize=(4, 7),
                                            legend=False)
    





