import streamlit as st
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
import plotly_express as px
import numpy as np
import requests
from Home import database
st.markdown("## Historical Weights ")
st.sidebar.markdown("#  Historical Weights ")
st.sidebar.image('https://i.postimg.cc/g0JMMBbp/LOGO-TAL-AVEC-SIGNATURE.png', use_column_width=True)

df = database

# --------------------------------------------------------------------------------- # 
# --------------------------Data production---------------------------------------- # 
# --------------------------------------------------------------------------------- # 

weights_m = pd.DataFrame([(1/df['USDCHF'])*100,(1/df['USDEUR'])*250,(1/df['USDGBP'])*50,(1/df['USDJPY'])*18000,(1/df['USDCNY'])*1600,(1/df['USDSGD'])*80,((df['GLDUSD'])*0.2)])
weights_m = weights_m.T
w_chf = weights_m['USDCHF'] / (df['TALUSD']*1000)
w_eur = weights_m['USDEUR'] / (df['TALUSD']*1000)
w_gbp = weights_m['USDGBP'] / (df['TALUSD']*1000)
w_jpy = weights_m['USDJPY'] / (df['TALUSD']*1000)
w_cny = weights_m['USDCNY'] / (df['TALUSD']*1000)
w_sgd = weights_m['USDSGD'] / (df['TALUSD']*1000)
w_gold = weights_m['GLDUSD'] / (df['TALUSD']*1000)
weights_daily = pd.DataFrame([w_chf,w_eur,w_gbp,w_jpy,w_cny,w_sgd,w_gold])
weights_daily = weights_daily.T
weights_daily.columns = ['CHF','EUR','GBP','JPY','CNY','SGD','GOLD']

# --------------------------------------------------------------------------------- #

col1, col2 = st.columns([3, 1])

@st.cache_data
def histo():
    fig_w = go.Figure()
    fig_w.add_trace(go.Scatter(x=pd.to_datetime(weights_daily.index, format='%d/%m/%Y %H:%M'),y=weights_daily['CHF'], name='CHF'))
    fig_w.add_trace(go.Scatter(x=pd.to_datetime(weights_daily.index, format='%d/%m/%Y %H:%M'),y=weights_daily['EUR'], name='EUR'))
    fig_w.add_trace(go.Scatter(x=pd.to_datetime(weights_daily.index, format='%d/%m/%Y %H:%M'),y=weights_daily['GBP'], name='GBP'))
    fig_w.add_trace(go.Scatter(x=pd.to_datetime(weights_daily.index, format='%d/%m/%Y %H:%M'),y=weights_daily['JPY'], name='JPY'))
    fig_w.add_trace(go.Scatter(x=pd.to_datetime(weights_daily.index, format='%d/%m/%Y %H:%M'),y=weights_daily['CNY'], name='CNY'))
    fig_w.add_trace(go.Scatter(x=pd.to_datetime(weights_daily.index, format='%d/%m/%Y %H:%M'),y=weights_daily['SGD'], name='SGD'))
    fig_w.add_trace(go.Scatter(x=pd.to_datetime(weights_daily.index, format='%d/%m/%Y %H:%M'),y=weights_daily['GOLD'], name='GOLD'))
    fig_w.update_layout(title='Basket components weights',      
                        width=1100,
        height=800)
    return fig_w

col1.plotly_chart(histo(), use_container_width=True)

w_date = col2.date_input('Select a date:',
                                 dt.date(2018, 3, 15))
w_date = w_date.strftime('%d/%m/%Y %H:%M')
specific_row = weights_daily.loc[w_date]

repartition = pd.DataFrame({'Currency': ['CHF', 'EUR', 'GBP', 'JPY', 'CNY', 'SGD', 'Gold'],
                            'Weights': [specific_row['CHF'], specific_row['EUR'], specific_row['GBP'], specific_row['JPY'], specific_row['CNY'], specific_row['SGD'], specific_row['GOLD']]})

fig_weights = px.pie(repartition, values='Weights', names='Currency', title='Basket components distribution')

col2.plotly_chart(fig_weights)