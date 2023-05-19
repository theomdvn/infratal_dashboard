import streamlit as st
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
import plotly_express as px
import numpy as np
from accueil import database
st.markdown("## Comparer TAL")
st.sidebar.markdown("# Comparer TAL")

def anyrate(df,from_currency,to_currency):
    x = (1/df[from_currency])*df[to_currency]
    return x
def XXXTAL(df, from_currency):
    x = (1/df[from_currency])*(1/df['TAL'])
    return x

df = database

df['EURUSD'] = 1/df['USDEUR']
df['GLDEUR'] = df['GLDUSD']*df['USDEUR']
df = df.loc[:, ~database.columns.str.startswith('USD')]
df.columns = df.columns.str.replace('EUR', '')
df.drop(columns=['TALUSD', 'GLDUSD'], inplace=True)

start_date = st.sidebar.date_input('Select start date:',
                                   dt.date(2018, 7, 17))


end_date = st.sidebar.date_input('Select end date:',
                                 dt.date(2023, 3, 17))

delta = end_date-start_date
start_date = start_date.strftime('%d/%m/%Y %H:%M')
end_date = end_date.strftime('%d/%m/%Y %H:%M')

liste_c = list(df.columns)

liste_c.remove('TAL')
liste_c.remove('GLD')

currencies = ['ALL'] + ['GOLD'] + ['EUR'] + liste_c

currency1 = ['EUR'] + liste_c

filtered_df = df.loc[start_date:end_date]

currency = st.sidebar.selectbox('Which currency are you protecting :', currency1)

checkbox = st.sidebar.checkbox('Compare TAL with another currency')
if checkbox:
    currency2 = st.sidebar.selectbox('Choose a currency into invest at date :', currencies)
else:
    currency2 = currency

col1, col2 = st.columns([3, 1])

fig = go.Figure()

if currency == 'EUR':
    fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=1/df['TAL'], name='EURTAL'))    
else:
    talqty = (XXXTAL(filtered_df,currency))
    fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'), y=talqty, name=f'{currency}TAL'))
    
    currency_qty = 1000*1/(XXXTAL(filtered_df,currency).tail(1).values[0])
    final_currency_qty = 1000*1/(XXXTAL(filtered_df,currency).head(1).values[0])
    percentage_difference = (final_currency_qty - currency_qty) / final_currency_qty * 100

    col2.markdown(f'# 1000 TAL on {start_date.split(" ")[0]} would cost you {round(currency_qty,2)} {currency}')

    col2.markdown("""---""")

    col2.markdown(f'# 1000 TAL on {end_date.split(" ")[0]} would cost you {round(final_currency_qty,2)} {currency}')

    col2.markdown("""---""")
    if percentage_difference > 0:
        col2.markdown(f'# {currency} has lost {round(percentage_difference,2)}% of its value in {delta.days} days when paired with TAL ')
    else:
        col2.markdown(f'# {currency} has won {-round(percentage_difference,2)}% of its value in {delta.days} days when paired with TAL ')


fig.update_layout(title='Currency Comparison',
                    xaxis_title='Date',
                    yaxis_title='Rate',
        width=1200,
        height=800
        )

col1.plotly_chart(fig)

st.markdown("""---""")