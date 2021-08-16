#!/usr/bin/env python
# coding: utf-8

# In[2]:


#pip install pandas_datareader


# In[2]:


from math import log, sqrt, pi, exp
from scipy.stats import norm
from datetime import datetime, date
import numpy as np
import pandas as pd
from pandas import DataFrame
import pandas_datareader.data as web


# ### Inputs needed
# * Stock Ticker: S
# * Strike Price: K
# * Expiration Date: expiry  
#   
# The rest can be calculated automatically

# In[40]:





# In[101]:


def calculate_inputs(stock,expiry,strike_price):
    '''
    this function has 2 purposes. 1 to cal
    '''
    today = datetime.now()
    one_year_ago = today.replace(year=today.year-1)
    global S
    try:
        ### Testing inputs
        df = web.DataReader(stock, 'yahoo', one_year_ago, today)
    except:
        return 'data call error'
    
    try:
        df = df.sort_values(by="Date")
        df = df.dropna()
        df = df.assign(close_day_before=df.Close.shift(1))
        df['returns'] = ((df.Close - df.close_day_before)/df.close_day_before)
    except:
        return 'transformation error'
    global sigma
    try:
        sigma = np.sqrt(252) * df['returns'].std()
    except:
        return 'sigma error'
    
    global r
    
    try:
        
        #this breaks on weekends because there is no data to pull on weekends
        r = (web.DataReader(
            "^TNX", 'yahoo', today.replace(day=today.day-1), today)['Close'].iloc[-1])/100
    except KeyError:
        r = (web.DataReader(
            "^TNX", 'yahoo', today.replace(day=today.day-2), today)['Close'].iloc[-1])/100
    except KeyError:
        r = (web.DataReader(
            "^TNX", 'yahoo', today.replace(day=today.day-3), today)['Close'].iloc[-1])/100
    else:
        return 'Risk Free Rate error'
    
    try:
        S = df['Close'].iloc[-1]
        
    except:
        return 'Current Stock Price error'
    global T
    try:
        T = (datetime.strptime(expiry, "%m-%d-%Y") - datetime.utcnow()).days / 365
    except:
        return 't error'


# In[129]:


def THE_GREEKS():
    print('Current Price: ',S, '   Time to Maturity: ', T)
    print('Volatility:    ',sigma, ' Risk-Free Rate: ', r)
    print('')
    print( 'The Call Price: ', bs_call())
    print('')
    print('Delta: ',call_delta(),'          Gamma: ',call_gamma())
    print('Vega:  ',call_vega(),'          Theta: ',call_theta())
    print('Rho:   ',call_rho())
    print('')
    print( 'The Put Price: ', bs_put())
    print('')
    print('Delta: ',put_delta(),'        Gamma: ',put_gamma())
    print('Vega:  ',put_vega(),'          Theta: ',put_theta())
    print('Rho:   ',put_rho())


# In[112]:


def d1():
    '''
    S: Current Stock Price
    K: Strike Price
    T: Time to maturity
    r: Risk-free interest rate
    sigma: Volatility/Standard Deviation of log returns

    returns: volatility weighted return rate
    '''
    try:
        x = log(S/K)
    except:
        return 'x error'
    try:
        y = (r+sigma**2/2.)*T
    except:
        return 'y error'
    try:
        z = (sigma*sqrt(T))
    except:
        return 'z error'
    return(x+y)/z

def d2():
    '''
    S: Current Stock Price
    K: Strike Price
    T: Time to maturity
    r: Risk-free interest rate
    sigma: Volatility/Standard Deviation of log returns

    returns: volatility weighted interest rate
    '''
    return d1()-sigma*sqrt(T)

###
def bs_call():
    '''
    S: Current Stock Price
    K: Strike Price
    T: Time to maturity
    r: Risk-free interest rate
    sigma: Volatility/Standard Deviation of log returns

    returns: Black-Sholes Call option price
    '''
    return S*norm.cdf(d1())-K*exp(-r*T)*norm.cdf(d2())
  
def bs_put():
    '''
    S: Current Stock Price
    K: Strike Price
    T: Time to maturity
    r: Risk-free interest rate
    sigma: Volatility/Standard Deviation of log returns

    returns: Black-Sholes Put option price
    '''
    return K*exp(-r*T)-S+bs_call()


# In[122]:


###
### Adding more information for additional analysis
def call_implied_volatility():
    sigma = 0.001
    while sigma < 1:
        Price_implied = S *             norm.cdf(d1(S, K, T, r, sigma))-K*exp(-r*T) *             norm.cdf(d2(S, K, T, r, sigma))
        if call_price-(Price_implied) < 0.001:
            return sigma
        sigma += 0.001
    return "Not Found"

def put_implied_volatility():
    sigma = 0.001
    while sigma < 1:
        Price_implied = K*exp(-r*T)-S+bs_call(S, K, T, r, sigma)
        if put_price-(Price_implied) < 0.001:
            return sigma
        sigma += 0.001
    return "Not Found"

###
### THE GREEKS @prestal33 
def call_delta():
    return norm.cdf(d1())
def call_gamma():
    return norm.pdf(d1())/(S*sigma*sqrt(T))
def call_vega():
    return 0.01*(S*norm.pdf(d1())*sqrt(T))
def call_theta():
    return 0.01*(-(S*norm.pdf(d1())*sigma)/(2*sqrt(T)) - r*K*exp(-r*T)*norm.cdf(d2()))
def call_rho():
    return 0.01*(K*T*exp(-r*T)*norm.cdf(d2()))

   
def put_delta():
    return -norm.cdf(-d1())
def put_gamma():
    return norm.pdf(d1())/(S*sigma*sqrt(T))
def put_vega():
    return 0.01*(S*norm.pdf(d1())*sqrt(T))
def put_theta():
    return 0.01*(-(S*norm.pdf(d1())*sigma)/(2*sqrt(T)) + r*K*exp(-r*T)*norm.cdf(-d2()))
def put_rho():
    return 0.01*(-K*T*exp(-r*T)*norm.cdf(-d2()))


# In[ ]:





# In[ ]:





# In[26]:


def sig(stock):
    today = datetime.now()
    one_year_ago = today.replace(year=today.year-1)
    try:
        ### Testing inputs
        df = web.DataReader(stock, 'yahoo', one_year_ago, today)
    except:
        return 'data call error'
    
    try:
        df = df.sort_values(by="Date")
        df = df.dropna()
        df = df.assign(close_day_before=df.Close.shift(1))
        df['returns'] = ((df.Close - df.close_day_before)/df.close_day_before)
    except:
        return 'transformation error'    
    try:
        sigma = np.sqrt(252) * df['returns'].std()
    except:
        return 'sigma error'
    return sigma


# In[130]:


### Testing Inputs 
st = 'TXT'
ex = '12-18-2022'
K = 70
calculate_inputs(st,ex,K)
THE_GREEKS()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




