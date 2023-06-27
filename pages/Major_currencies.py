import streamlit as st
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
import plotly_express as px
import numpy as np
import requests
import json
from Home import database

df = database
df['EURUSD'] = 1/df['USDEUR']
df['GLDEUR'] = df['GLDUSD']*df['USDEUR']
df = df.loc[:, ~database.columns.str.startswith('USD')]
df.columns = df.columns.str.replace('EUR', '')
df.drop(columns=['TALUSD', 'GLDUSD'], inplace=True)
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image('https://i.postimg.cc/g0JMMBbp/LOGO-TAL-AVEC-SIGNATURE.png')
def XXXTAL(df, from_currency):
    x = (1/df[from_currency])*(1/df['TAL'])
    return x

start_date = st.sidebar.date_input('Start date:', dt.date(2016, 3, 15))

end_date = dt.date.today() - dt.timedelta(days=1)

filtered_df = df.loc[start_date:end_date]

fig =  go.Figure()

# Line filled with zeros, with flashy color
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'), y=np.zeros(len(filtered_df.index)), name='sTAL', line=dict(color='lightblue')))

prices = 1/filtered_df['TAL']

variations = (prices - prices.iloc[0]) / prices.iloc[0]
# Other traces, with more muted colors
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=variations, name='€', line=dict(color='darkblue')))
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=(XXXTAL(filtered_df,'USD') - XXXTAL(filtered_df,'USD').iloc[0]) / XXXTAL(filtered_df,'USD').iloc[0], name='$'))
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=(XXXTAL(filtered_df,'CHF') - XXXTAL(filtered_df,'CHF').iloc[0]) / XXXTAL(filtered_df,'CHF').iloc[0], name='CHF'))
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=(XXXTAL(filtered_df,'GBP') - XXXTAL(filtered_df,'GBP').iloc[0]) / XXXTAL(filtered_df,'GBP').iloc[0], name='£'))
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=(XXXTAL(filtered_df,'JPY') - XXXTAL(filtered_df,'JPY').iloc[0]) / XXXTAL(filtered_df,'JPY').iloc[0], name='JPY'))
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=(XXXTAL(filtered_df,'CNY') - XXXTAL(filtered_df,'CNY').iloc[0]) / XXXTAL(filtered_df,'CNY').iloc[0], name='CNY'))
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=(XXXTAL(filtered_df,'SGD') - XXXTAL(filtered_df,'SGD').iloc[0]) / XXXTAL(filtered_df,'SGD').iloc[0], name='SGD'))

fig.update_layout(title='The Resilience of sTAL Against Single Currency Depreciation', xaxis_title='Date', height=800)



fig2 =  go.Figure()
fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'), y=np.zeros(len(filtered_df.index)), name='sTAL', line=dict(color='lightblue')))

fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=(XXXTAL(filtered_df,'BRL') - XXXTAL(filtered_df,'BRL').iloc[0]) / XXXTAL(filtered_df,'BRL').iloc[0], name='BRL'))
fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=(XXXTAL(filtered_df,'CAD') - XXXTAL(filtered_df,'CAD').iloc[0]) / XXXTAL(filtered_df,'CAD').iloc[0], name='CAD'))
fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=(XXXTAL(filtered_df,'TRY') - XXXTAL(filtered_df,'TRY').iloc[0]) / XXXTAL(filtered_df,'TRY').iloc[0], name='TRY'))
fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=(XXXTAL(filtered_df,'INR') - XXXTAL(filtered_df,'INR').iloc[0]) / XXXTAL(filtered_df,'INR').iloc[0], name='INR'))
fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=(XXXTAL(filtered_df,'KRW') - XXXTAL(filtered_df,'KRW').iloc[0]) / XXXTAL(filtered_df,'KRW').iloc[0], name='KRW'))
fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=(XXXTAL(filtered_df,'MXN') - XXXTAL(filtered_df,'MXN').iloc[0]) / XXXTAL(filtered_df,'MXN').iloc[0], name='MXN'))
fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=(XXXTAL(filtered_df,'ZAR') - XXXTAL(filtered_df,'ZAR').iloc[0]) / XXXTAL(filtered_df,'ZAR').iloc[0], name='ZAR'))


fig2.update_layout(title='sTAL : A Defense Against Value Depreciation in Emerging Market Currencies', xaxis_title='Date', height=800)

st.plotly_chart(fig, use_container_width=True)

st.markdown('---')

st.plotly_chart(fig2, use_container_width=True)