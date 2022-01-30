import json
import statistics
from symtable import Symbol
import pandas as pd
import btalib, os, account_requests, datetime

import account_requests
class Ta:

    def __init__(self,active) -> None:
        self.symbols = active

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # Data Holders 
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #files = os.listdir('ohlc')             # list of filenames in specified directory
    # symbols = []                            # list of stock symbols
    all_df = {}                             # Dict of data frames with stock data (symbol is index)
    #current_strategy = ['rsi','ema']
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

    Bot = account_requests.bot()  # Alpaca-api object

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # Momentum Indicators
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    all_momentum = {}                   # Dictionary for the current momentum indicator being used, if any  

    def set_rsi(self,symbol):                    # Relative strength index. Default period: 14  
        self.all_momentum[symbol] \
            = btalib.rsi(self.all_df[symbol], period=14)
        self.all_momentum[symbol].df.reset_index(inplace=True)   # want normal indexing

    def set_macd(self,symbol):                   # Moving Average Convergence Divergence. Slow period: 26 
        self.all_momentum[symbol] \
            = btalib.macd(self.all_df[symbol])
        self.all_momentum[symbol].df.reset_index(inplace=True)
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # Trend Indicators
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    all_trend = {}                      # Dictionary for the current trend indicator being used, if any

    def set_ema(self,symbol, tf):                        # Exponential moving average. Period: 30
        self.all_trend[symbol] \
            = btalib.ema(self.all_df[symbol], period=100)
        self.all_trend[symbol].df.reset_index(inplace=True)
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # Volume Indicators
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    all_volume = {}                     # Dictionary for the current volume indicator being used, if any        

    def set_obv(self,symbol):                    # On-balance volume. Default period: 1
        self.all_volume[symbol] \
            = btalib.obv(self.all_df[symbol])
        self.all_volume[symbol].df.reset_index(inplace=True)
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # Volatility Indicators
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    all_volatility = {}                 # Dictionary for the current volatiliry indicator being used, if any

    def set_bbands(self,symbol):                         # Bollinger bands. Default period: 20
        self.all_volatility[symbol] \
            = btalib.bbands(self.all_df[symbol])
        self.all_volatility[symbol].df.reset_index(inplace=True)
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # Strategies
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def reset_strategy_param(self):
        self.all_momentum = {}
        self.all_trend = {}
        self.all_volatility = {}
        self.all_volume = {}


    def rsi_ema(self):
        #order = {}
        for s in self.symbols:
            self.set_ema(s,100)
            self.set_rsi(s)
            for (o,c,e,r) in zip(self.all_df[s].Open,self.all_df[s].Close\
                ,self.all_trend[s].df.ema,self.all_momentum[s].df.rsi):
                delta = statistics.mean([o,c]) - e # mean bar price  - ema
                if delta > 0 and r > 50:    # need to figure out when it crosses, not just when above
                    self.Bot.submit_buy(s,1)
                    #order['buy':self.all_df[s].Date]
                elif delta < 0 and r < 50:
                    self.Bot.submit_sell(s,1)    # probably should take into account previous orders and sell those too
                    #order['sell':self.all_df[s].Date]
                else:
                    # do nothing
                    pass
        #return order
            
                
    # sell when obv crosses ema downward. Buy when obv crosses ema upward
    def ema_obv(self):
        for s in self.symbols:
            self.set_ema(s,100)
            self.set_obv(s)
            for (e,o) in zip(self.all_trend[s].df.ema, self.all_volume[s].df.obv):
                pass
            for i in range(len(self.all_trend[s].df.ema)):
                delta = self.all_volume[s].df.obv[i] - self.all_trend[s].df.ema[i]
            # if delta > 0.1*
                pass

    def ema_bbands(self):
        pass

    def macd_obv(self):
        pass

    def rsi_bbands(self):
        pass

    def obv_bbands(self):
        pass
    
    def dca(self):
        for s in self.symbols:
            for d in self.all_df[s].Date:
                current_date = datetime.datetime.strptime(d,'%Y-%m-%dT%H:%M:%SZ')
                most_recent = self.Bot.api.list_orders(status='open',limit=1).submitted_at   # change this in future

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *       

    def execute(self,current_strategy):
        self.reset_strategy_param()

        for s in self.symbols:
            self.all_df[s] \
                = pd.read_csv('ohlc/{}.txt'.format(s), parse_dates=True, index_col='Date')
            
        eval('self.{}()'.format(current_strategy))
        # eval work when called from another file?
            # make work with sleep
        #for filename in self.files:
            # Get bar data from files
         #   key = filename[0:-4]                # symbols[] is formed from file names
          #  self.symbols.append(key)
           # self.all_df[key] \
            #    = pd.read_csv('ohlc/{}'.format(filename), parse_dates=True, index_col='Date')

        # call the appropriate strategy  modify this to work w string or smth
        #eval('self.'+'_'.join(current_strategy) + '()')



#t = Ta(['MSFT','AAPL','AMZN'])
#t.execute('rsi_ema')
#print(t.all_momentum['MSFT'].df)