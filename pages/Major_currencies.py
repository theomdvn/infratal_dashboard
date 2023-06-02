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
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=(1/filtered_df['TAL']).pct_change().cumsum(), name='€'))
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=XXXTAL(filtered_df,'USD').pct_change().cumsum(), name='$'))
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=XXXTAL(filtered_df,'CHF').pct_change().cumsum(), name='CHF'))
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=XXXTAL(filtered_df,'GBP').pct_change().cumsum(), name='£'))
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=XXXTAL(filtered_df,'JPY').pct_change().cumsum(), name='JPY'))
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=XXXTAL(filtered_df,'CNY').pct_change().cumsum(), name='CNY'))
fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=XXXTAL(filtered_df,'SGD').pct_change().cumsum(), name='SGD'))
fig.update_layout( xaxis_title='Date', height=800)

fig2 =  go.Figure()
fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=XXXTAL(filtered_df,'BRL').pct_change().cumsum(), name='BRL'))
fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=XXXTAL(filtered_df,'CAD').pct_change().cumsum(), name='CAD'))
fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=XXXTAL(filtered_df,'TRY').pct_change().cumsum(), name='TRY'))
fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=XXXTAL(filtered_df,'INR').pct_change().cumsum(), name='INR'))
fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=XXXTAL(filtered_df,'KRW').pct_change().cumsum(), name='KRW'))
fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=XXXTAL(filtered_df,'MXN').pct_change().cumsum(), name='MXN'))
fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=XXXTAL(filtered_df,'ZAR').pct_change().cumsum(), name='ZAR'))


fig2.update_layout( xaxis_title='Date', height=800)

st.plotly_chart(fig, use_container_width=True)

st.markdown('---')

st.plotly_chart(fig2, use_container_width=True)