import streamlit as st
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
import plotly_express as px
import numpy as np
from Accueil import database
st.markdown("## Compare TAL")
st.sidebar.markdown("# Compare TAL")
st.sidebar.image('https://i.postimg.cc/g0JMMBbp/LOGO-TAL-AVEC-SIGNATURE.png', width=200)

@st.cache_data
def anyrate(df,from_currency,to_currency):
    x = (1/df[from_currency])*df[to_currency]
    return x

@st.cache_data
def XXXTAL(df, from_currency):
    x = (1/df[from_currency])*(1/df['TAL'])
    return x

@st.cache_data
def qtytal(df, from_currency):
    x = 1000*(df[from_currency])*df['TAL'][0]
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

qty = 1000

fig = go.Figure()


if currency == 'EUR':
    
    fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=1000*filtered_df['TAL'], name='TALEUR'))
    
    currency_qty_1 = 1000*(filtered_df['TAL'].head(1).values[0]) #Value of 1000 TAL in EUR at day 0
    final_currency_qty = 1000*(filtered_df['TAL'].tail(1).values[0])
    percentage_difference = (final_currency_qty - currency_qty_1) / final_currency_qty * 100

    data = 1/filtered_df['TAL']
    data = data.pct_change()
    eur_qty = round(currency_qty_1,2)
    
else:

    talqty = 1/(XXXTAL(filtered_df,currency))*1000

    fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'), y=talqty, name=f'TAL{currency}'))
    
    currency_qty_1 = 1000*1/(XXXTAL(filtered_df,currency).head(1).values[0])
    final_currency_qty = 1000*1/(XXXTAL(filtered_df,currency).tail(1).values[0])
    percentage_difference = (final_currency_qty - currency_qty_1) / final_currency_qty * 100

    # col2.markdown(f' 1000 TAL on {start_date.split(" ")[0]} would cost you {round(currency_qty,2)} {currency}')

    # col2.markdown("""---""")

    # col2.markdown(f' 1000 TAL on {end_date.split(" ")[0]} would cost you {round(final_currency_qty,2)} {currency}')

    # col2.markdown("""---""")
    # if percentage_difference > 0:
    #     col2.markdown(f' {currency} has lost {round(percentage_difference,2)}% of its value in {delta.days} days when paired with TAL ')
    # else:
    #     col2.markdown(f' {currency} has won {-round(percentage_difference,2)}% of its value in {delta.days} days when paired with TAL ')
    
    data = talqty
    data = data.pct_change()

compare = pd.DataFrame()

if currency2 == 'ALL' and currency == 'EUR':
    for i in filtered_df.columns:
        if i != 'TAL' and i != 'GLD':
            compare[f'{currency}{i}'] = filtered_df[i].pct_change()


elif currency2 == 'ALL' and currency != 'EUR':
    
    for i in filtered_df.columns:
        currency_qty = anyrate(filtered_df.iloc[0].T,currency,i)
        cur2_cur = currency_qty*anyrate(filtered_df,i,currency)
        if i != 'TAL' and i != 'GLD':
            compare[f'{currency}{i}'] = cur2_cur.pct_change()

elif currency2 == 'GOLD' and currency == 'EUR':
    gold_qty_eur = currency_qty_1*(1/filtered_df['GLD'].head(1).values[0]) # How much oz of gold you can buy with 1000 TAL at day 0
    gldeur = gold_qty_eur*(filtered_df['GLD'])
    fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'), y=gldeur, name=f'{currency2}/{currency}'))
    compare[f'{currency2}{currency}'] = gldeur.pct_change()
    final_qty_cur =  gldeur.tail(1).values[0]

elif currency2 == 'GOLD' and currency != 'EUR':
    gold_qty_cur = currency_qty_1*(1/filtered_df[currency].head(1).values[0])*(1/filtered_df['GLD'].head(1).values[0]) # How much oz of gold you can buy with 1000 TAL at day 0
    gldcur = (gold_qty_cur*(filtered_df['GLD']))*(filtered_df[currency])
    fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'), y=gldcur, name=f'{currency2}/{currency}'))
    compare[f'{currency2}{currency}'] = gldcur.pct_change()
    final_qty_cur =  gldcur.tail(1).values[0]

elif currency2 != 'ALL' and currency == 'EUR' and currency2 != 'GOLD':
     if currency2 != 'EUR':
        currency_qty = eur_qty*(filtered_df[currency2][0])

        cur2_cur = currency_qty*(1/filtered_df[currency2])

        fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'), y=cur2_cur, name=f'{currency2}{currency}'))
        final_qty_cur =  cur2_cur.tail(1).values[0] 
        compare[f'{currency}{currency2}'] = filtered_df[currency2].pct_change()


elif currency2 != 'ALL' and currency != 'EUR' and currency2 != 'GOLD' and currency2 != currency:

    # 1000 TAL -> currency 2 at day 0
    currency_qty = talqty.head(1).values[0]*anyrate(filtered_df.iloc[0].T,currency,currency2)

    # 1000 TAL in currency 2 for x days

    cur2_cur = currency_qty*(anyrate(filtered_df,currency2,currency)) 
    
    fig.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'), y=cur2_cur, name=f'{currency2}{currency}'))
    final_qty_cur =  cur2_cur.tail(1).values[0] 
    compare[f'{currency}{currency2}'] = cur2_cur.pct_change()



fig.update_layout(title='Currency Comparison',
                    xaxis_title='Date',
                    yaxis_title='Rate',
                    height=800
        )

st.plotly_chart(fig,  use_container_width=True)

st.markdown(f'*This graph represent the value of 1000 TAL in {currency}*')

if st.checkbox(f'See change rate for {currency}/TAL'):
    fig2 = go.Figure()

    if currency == 'EUR':
    
        fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'),y=1/filtered_df['TAL'], name='EURTAL'))
    
    else:
        fig2.add_trace(go.Scatter(x=pd.to_datetime(filtered_df.index, format='%d/%m/%Y %H:%M'), y=(XXXTAL(filtered_df,currency)), name=f'{currency}TAL'))
    
    fig2.update_layout(title=f'Currency rate for {currency}/TAL',
                        xaxis_title='Date',
                        yaxis_title='Rate',
            height=800
            )

    st.plotly_chart(fig2,  use_container_width=True)
st.markdown("""---""")
st.markdown(f' 1000 TAL on {start_date.split(" ")[0]} would have costed you {round(currency_qty_1,2)} {currency}')
st.markdown(f' 1000 TAL on {end_date.split(" ")[0]} would bring you {round(final_currency_qty,2)} {currency}')
if percentage_difference > 0:
        st.markdown(f' {currency} has lost {round(percentage_difference,2)}% of its value in {delta.days} days when paired with TAL ')
else:
        st.markdown(f' {currency} has won {-round(percentage_difference,2)}% of its value in {delta.days} days when paired with TAL ')

if checkbox and currency2 != 'ALL':
    st.markdown("""---""")
    st.markdown(f' If you changed {round(currency_qty_1,2)} {currency} in {currency2}, you would have {round(final_qty_cur,2)} {currency} at the end of the period')
    percentage_difference_2 = (final_qty_cur - currency_qty_1) / final_qty_cur * 100

    if percentage_difference_2 > 0:
            st.markdown(f' {currency} has lost {round(percentage_difference_2,2)}% of its value in {delta.days} days when changed in {currency2} ')
    else:
            st.markdown(f' {currency} has won {-round(percentage_difference_2,2)}% of its value in {delta.days} days when changed in {currency2} ')
st.markdown("""---""")
# --- Statistics --- #

statistics_df = pd.DataFrame({
        'Currency': [f'TAL{currency}'],
        'Mean Return': [data.mean()],
        'Standard Deviation': [data.std()],
        'VaR': [data.quantile(0.05)],
        'ES': [data[data <= data.quantile(0.05)].mean()],
        'Max Drawdown': [data.min()],
        })
statistics_df.set_index('Currency', inplace=True)
st.markdown("<h1 style='font-size:18px;'>Statistics : </h1>", unsafe_allow_html=True)
st.dataframe(statistics_df)

if checkbox:
    statistics_compare = compare.describe()
    statistics_compare.loc['VAR'] = compare.quantile(0.05)
    statistics_compare.loc['ES'] = compare[compare <= compare.quantile(0.05)].mean()
    statistics_compare = statistics_compare.T
    statistics_compare = statistics_compare.drop(columns=['count', '25%', '50%', '75%'])
    statistics_compare = statistics_compare.rename(columns={'mean': 'Mean Return', 'std': 'Standard Deviation', 'min': 'Max Drawdown', 'max': 'Max Return'})
    st.markdown("""---""")
    st.dataframe(statistics_compare)




if st.checkbox('Learn more about statistics'):
    st.markdown('---')
    st.markdown('## Mean Return')
    st.markdown("Rendement moyen) : Il s'agit de la moyenne des rendements d'un investissement sur une période donnée. Cela indique la performance moyenne d'un investissement sur cette période.")
    st.markdown('---')
    st.markdown('## Standard Deviation')
    st.markdown("(Écart-type) : C'est une mesure de la dispersion des rendements d'un investissement par rapport à son rendement moyen. Plus l'écart-type est élevé, plus les rendements peuvent varier de manière significative par rapport à la moyenne.")
    st.markdown('---')
    st.markdown('## VaR')
    st.markdown("(Value at Risk) : La VaR (ou valeur en risque) est une mesure statistique qui estime les pertes potentielles maximales (en termes de valeur monétaire) auxquelles un investissement ou un portefeuille peut être exposé, avec un certain niveau de confiance et sur une certaine période. Par exemple, une VaR de 5% à un horizon de 1 jour indique que les pertes ne dépasseront pas un certain montant avec une probabilité de 95% sur une journée.")
    st.markdown('---')
    st.markdown('## ES')
    st.markdown("(Expected Shortfall) : L'ES (ou rendement espéré en cas de perte) est une autre mesure du risque qui complète la VaR. Il représente la moyenne des pertes qui dépassent la VaR. Par exemple, si la VaR est de 10 000 € avec une probabilité de 95%, l'ES pourrait être de 15 000 €, ce qui signifie que si les pertes dépassent la VaR, elles sont en moyenne de 15 000 €.")
    st.markdown('---')
    st.markdown('## Max Drawdown a 1 jour')
    st.markdown("(Perte maximale) : Il s'agit de la plus grande baisse en pourcentage du prix en une journée.")