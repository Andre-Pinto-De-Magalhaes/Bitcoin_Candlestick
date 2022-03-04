'''Program will retrive data on bitcoin from Coin Gecko to create a candlestick
chart that tracks the prices of bitcoin over a period of 30 days'''

import pandas as pd
from pycoingecko import CoinGeckoAPI 
import plotly.graph_objects as go


#initialize class/object
cg = CoinGeckoAPI()


######## Get data from Coin Gecko#######
#retrieves data on bitcoin in 30 day time period
bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency = 'usd', days = 30)

bc_price_data = bitcoin_data['prices']

#######organize data and convert values to readable data#####

data = pd.DataFrame(bc_price_data, columns = ['TimeStamp', 'Price'])

data['Date'] = pd.to_datetime(data['TimeStamp'], unit=('ms'))





#########Create candlestick chart with data############

#Groups data by date to get daily min, max, open price and closing price
candlestick_data = data.groupby(data.Date.dt.date).agg({'Price':['min','max','first','last' ]})




print(candlestick_data)
print(candlestick_data.describe())

fig = go.Figure(data = [go.Candlestick(x = candlestick_data.index,
               open = candlestick_data['Price']['first'],
               high = candlestick_data['Price']["max"],
               low = candlestick_data['Price']['min'],
               close = candlestick_data['Price']['last'])
                        ])

fig.update_layout(xaxis_rangeslider_visible = False, xaxis_title = 'Date',
                  yaxis_title = 'Price(USD$)', title = 'Bitcoin Prices over 30 days')
               
fig.update_traces(legendgrouptitle_font_size=20, selector=dict(type='candlestick'))

fig.write_html('Bitcoin price over 30 days.html', auto_open = True)