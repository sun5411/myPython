import pandas as pd
from pandas import Series,DataFrame
import pandas.io.data as web

all_data = {}
for ticker in ['AAPL','IBM','MSFT','YHOO']:
    all_data[ticker] = web.get_data_yahoo(ticker,'11/1/2015','11/11/2015')

price = DataFrame({tic:data['Adj Close']
                    for tic,data in all_data.iteritems()})

print price
