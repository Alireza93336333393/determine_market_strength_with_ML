import pandas as pd
import pandas_ta as ta 
class Gann_ML:
    def __init__(self,df:pd.DataFrame):
        self.df = df

    def is_high(self,df, i):
        is_high_val = False
        if df['Close'].iloc[i] < df['Open'].iloc[i]:
            for j in range(1, 11):
                if i + j >= len(df):
                    break
                if df['Close'].iloc[i+j] > df['Open'].iloc[i+j]:
                    is_high_val = True
                    break
        return is_high_val

    def is_low(self,df, i):
        is_low_val = False

        if df['Close'].iloc[i] > df['Open'].iloc[i]:
            for j in range(1, 11):
                if i + j >= len(df):
                    break
                if df['Close'].iloc[i+j] < df['Open'].iloc[i+j]:
                    is_low_val = True
                    break
        return is_low_val

    def generate_extremes(self):
        signals = pd.DataFrame(index=self.df.index, columns=['Signal'])
        signals['Signal'] = 0
        previous_signal = 0

        for i in range(len(self.df.index)):
            current_high = self.is_high(self.df,i)
            current_low = self.is_low(self.df,i)
            current_signal = 0
            if current_high:
                current_signal = -1

            elif current_low:
                current_signal = 1

            if current_signal != 0:
                if previous_signal == -1 and current_signal == 1:
                    signals['Signal'].iloc[i - 1] = -1 
                elif previous_signal == 1 and current_signal == -1:
                    signals['Signal'].iloc[i - 1] = 1
            previous_signal = current_signal
                

        self.df['extrem_points'] = signals['Signal']

    def up_and_down_days(self,bars:pd.DataFrame):
        bars['up_down_day'] = 0# up day is 1 down day is -1 and if inside day or outside day it would be 0 

        previous_low = bars['Low'].shift(1)
        previous_high = bars['High'].shift(1)

        up_days = (bars['Low'] > previous_low) & ( bars['High'] > previous_high)#if true its a up_day 
        bars.loc[up_days,'up_down_day'] = 1

        down_days = (bars['Low'] < previous_low) & ( bars['High'] <= previous_high)#if true its a down_day
        bars.loc[down_days,'up_down_day'] = -1
        


    def gann_swing_signals(self):

        signals = []
        for i in range(len(self.df.index)):
            signals.append(0) #initializes all signals to 0.

        for i in range(len(self.df.index)):
        
            if self.df['up_down_day'].iloc[i] == 1 and self.df['up_down_day'].iloc[i - 1] == -1:#down day to up day
                signals[i] = 0.5
            elif self.df['up_down_day'].iloc[i] == -1 and self.df['up_down_day'].iloc[i - 1] == 1:#up day to down day
                signals[i] = -0.5
            elif self.df['up_down_day'].iloc[i] == 1 and self.df['up_down_day'].iloc[i - 1] == 1:#up day to up day 
                signals[i] = 0.5
            elif self.df['up_down_day'].iloc[i] == -1 and self.df['up_down_day'].iloc[i - 1] == -1:#down day to down day 
                signals[i] = -0.5
            elif self.df['up_down_day'].iloc[i] == 1 and self.df['up_down_day'].iloc[i - 1] == 0:#flat day to up day 
                signals[i] = 0.5
            elif self.df['up_down_day'].iloc[i] == -1 and self.df['up_down_day'].iloc[i - 1] == 0:#falt day to down day
                signals[i] = -0.5
        return signals


    def extrem_signal_points(self):

        if 'extrem_points' not in self.df.columns:
            raise ValueError(f'extrem_points not in columns:{self.df.columns}')
        
        self.df['extrem_signals'] = 0

        for i in range(len(self.df.index)):

            if self.df['extrem_points'].iloc[i] == -1:#if extrem_up_point the price gone fall
                self.df['extrem_signals'].iloc[i] = -0.5

            elif self.df['extrem_points'].iloc[i] == 1:#if extrem_down_point the price gone raise
                self.df['extrem_signals'].iloc[i] = 0.5 


    def rsi_signals(self):
        self.df.ta.rsi(length=14, append=True)
        self.df.ta.rsi(length=7, append=True)
        self.df.fillna(0,inplace=True)
        #80/20  Rull for RSI_7 and 70/30 rull for RSI_14
        self.df['RSI_signals'] = 0
        for i in range(len(self.df.index)):
                if self.df['RSI_14'].iloc[i] == 0 or self.df['RSI_7'].iloc[i] == 0:#to skip the 0 values !
                    continue

                elif self.df['RSI_14'].iloc[i] <= 30 and self.df['RSI_7'].iloc[i] <= 20:#if both at oversold level then +0.5
                    self.df['RSI_signals'].iloc[i] = 0.5

                elif self.df['RSI_14'].iloc[i] >=70 and self.df['RSI_7'].iloc[i] >= 80:#if both at overbought level then -0.5 
                    self.df['RSI_signals'].iloc[i] = -0.5

    def generate_signals(self):
        self.df['high_low_signal'] = 0  # Initialize signal column

 
        buy_signals = (self.df['Close'] > self.df['feature_gann_hiLo']) & (self.df['Close'].shift(1) <= self.df['feature_gann_hiLo'].shift(1))
        self.df.loc[buy_signals, 'high_low_signal'] = 0.5  # 0.5 represents 'strong trend'

     
        sell_signals = (self.df['Close'] < self.df['feature_gann_hiLo']) & (self.df['Close'].shift(1) >= self.df['feature_gann_hiLo'].shift(1))
        self.df.loc[sell_signals, 'high_low_signal'] = -0.5  # -0.5 represents 'weak trend'

        self.df.loc[(self.df['high_low_signal'] != 1) & (self.df['high_low_signal'] != -1), 'high_low_signal'] = 0

        return self.df

            
