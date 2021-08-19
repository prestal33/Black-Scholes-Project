from datetime import date
import pandas_datareader as web
import datetime
import numpy as np
import pandas as pd
from math import log, sqrt, pi, exp
from scipy.stats import norm

class calculate_inputs:
    def __init__(self,
            stock: str,
            expiry: date,
            strike_price: float
        ):

        self.today = datetime.date.today()
        self.one_year_ago = self.today.replace(year=self.today.year-1)
        self.strike_price = strike_price
        
        ### Testing inputs
        df = web.DataReader(stock, 'yahoo', self.one_year_ago, self.today)

        df = df.sort_values(by="Date")
        df = df.dropna()
        df = df.assign(close_day_before=df.Close.shift(1))
        df['returns'] = ((df.Close - df.close_day_before)/df.close_day_before)
        
        self.sigma = np.sqrt(252) * df['returns'].std()
        
        self.r = (web.DataReader(
            "^TNX", 'yahoo', self.today.replace(day=self.today.day-1), self.today)['Close'].iloc[-1])/100
        
        self.S = df['Close'].iloc[-1]
            
        self.T = (datetime.datetime.strptime(str(expiry), "%m/%d/%Y").date() - self.today).days / 365
    
    def d1(self):
        '''
        returns: volatility weighted return rate
        '''
        return (log(self.S/self.strike_price)+(self.r+self.sigma**2/2.)*self.T)/(self.sigma*sqrt(self.T))
    def d2(self):
        '''
        returns: volatility weighted interest rate
        '''
        return self.d1()-self.sigma*sqrt(self.T)

    def price(self):
        '''
        returns: Black-Sholes Call option price
        '''
        return (self.S*norm.cdf(self.d1())-self.strike_price*exp(-self.r*self.T)*norm.cdf(self.d2()))
