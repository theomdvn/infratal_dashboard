import streamlit as st
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
import plotly_express as px
import numpy as np
import requests
import json
from Home import currency_country_map
from Home import database

st.write('## Pricer Wise')
st.sidebar.write('# Pricer Wise')
st.sidebar.image('https://i.postimg.cc/g0JMMBbp/LOGO-TAL-AVEC-SIGNATURE.png', use_column_width=True)

def conversion(from_currency, to_currency, amount):
    if from_currency == to_currency:
        return 1*amount
    amount = float(amount)
    
    url = f"https://www.boursorama.com/bourse/devises/convertisseur-devises/convertir?from={from_currency}%2F{currency_country_map.get(from_currency)}&to={to_currency}%2F[{currency_country_map.get(to_currency)}]&amount={amount}&showSpotLink=1"
    response = requests.get(url)
    if response.status_code == 200:
        response_text = response.text
        response_data = json.loads(response_text)
        #converted_amount = response_data["convertedAmount"]

        # Print the values
        #print("Converted Amount:", converted_amount)
        #print("Rate:", rate)
    else:
        st.warning('BOURSORAMA API DID NOT RESPOND')
        st.write(response.status_code)
    return round(float((response_data["convertedAmount"])),2)

def rate_TAL_to_currency(currency):
    goldamount_in_usd = float(database.tail(1)['GLDUSD'] * 0.2)
    #https://or.fr/api/spot-prices?metal=XAU&currency=EUR&weight_unit=oz&boundaries=1
    if currency == 'USD':
        rate = conversion('CHF',currency,100) + conversion('EUR',currency,250) + conversion('GBP',currency,50) + conversion('JPY',currency,18000) + conversion('CNY',currency,1600) + conversion('SGD',currency,80) + goldamount_in_usd
    else:
        rate = conversion('CHF',currency,100) + conversion('EUR',currency,250) + conversion('GBP',currency,50) + conversion('JPY',currency,18000) + conversion('CNY',currency,1600) + conversion('SGD',currency,80) + conversion('USD',currency,goldamount_in_usd)
    
    return rate*0.001 

def rate_currency_to_TAL(currency):
    return float(1/rate_TAL_to_currency(currency))

def conversion_with_fees(from_currency,to_currency,amount):
    r = requests.get(f'https://api.wise.com/v1/comparisons/provider/wise?sourceCurrency={from_currency}&sendAmount={amount}&targetCurrency={to_currency}')
    
    if r.status_code == 200:
        data = r.json()
        received_amount = None
        fee = None
        for route in data['routes']:
            if route['sourceCurrency'] == from_currency and route['targetCurrency'] == to_currency:
                received_amount = route['quotes'][0]['receivedAmount']
                fee = route['quotes'][0]['fee']
                break
    else:
        st.warning('WISE API DID NOT RESPOND')
        st.write(r.status_code)
    return fee,received_amount

# ------------------------------------------------------------#


left_column, right_column = st.columns(2)

# Add content to the left column
with left_column:
    left_column.header('Entering TAL')
    currency = st.selectbox('Choose a currency to convert in TAL:', ['EUR','USD'] + list(currency_country_map.keys()))
    qty = st.number_input('Select quantity to protect :', min_value=0, max_value=1000000000, value = 1000, step=1000)
    if qty == "":
        qty = 0
    output_amount = round(rate_currency_to_TAL(currency)*float(qty),2)
    
    #st.markdown('<body> <I> <p style="color:lightblue ";>This amount is without entry fees.</p></I></body>', unsafe_allow_html=True)
    chf = output_amount*100/1000
    eur = output_amount*250/1000
    gbp = output_amount*50/1000
    jpy = output_amount*18000/1000
    cny = output_amount*1600/1000
    sgd = output_amount*80/1000
    usd = output_amount*float(database.tail(1)['GLDUSD'] * 0.2)/1000
    gold = usd/float(database.tail(1)['GLDUSD'])

    data = pd.DataFrame({'Entry currency ': [currency], 'Entry amount ': [qty], 'TAL amount ': [output_amount]})
    repartition = pd.DataFrame({'Currency': ['CHF', 'EUR', 'GBP', 'JPY', 'CNY', 'SGD', 'Gold oz'],
                            'Amount': [round(chf,2), round(eur,2), round(gbp,2), round(jpy,2), round(cny,2), round(sgd,2), gold],
                            f'Amount in {currency}': [conversion('CHF',currency,chf), conversion('EUR',currency,eur), conversion('GBP',currency,gbp), conversion('JPY',currency,jpy), conversion('CNY',currency,cny), conversion('SGD',currency,sgd), conversion('USD',currency,usd)],
                            'Fees (in absolute value)':[conversion_with_fees('CHF',currency,chf)[0], conversion_with_fees('EUR',currency,eur)[0], conversion_with_fees('GBP',currency,gbp)[0], conversion_with_fees('JPY',currency,jpy)[0], conversion_with_fees('CNY',currency,cny)[0], conversion_with_fees('SGD',currency,sgd)[0], conversion_with_fees('USD',currency,usd)[0]],
                            f'Amount in {currency} with fees':[conversion_with_fees('CHF',currency,chf)[1], conversion_with_fees('EUR',currency,eur)[1], conversion_with_fees('GBP',currency,gbp)[1], conversion_with_fees('JPY',currency,jpy)[1], conversion('CNY',currency,cny), conversion_with_fees('SGD',currency,sgd)[1], conversion_with_fees('USD',currency,usd)[1]]})

    sum = repartition[f'Amount in {currency} with fees'].sum()
    
    st.markdown('*WITHOUT COMISSION*')

    st.write(f"Theorical amount : {output_amount} TAL")
    st.write(f'Amount with fees : {round(rate_currency_to_TAL(currency)*sum,2)} TAL')

    st.markdown('---')

    st.markdown('*WITH COMISSION (3%)*')
    st.write(f"Comission collected : {0.03*qty} {currency} or {conversion_with_fees(currency,'CHF',0.03*qty)[1]} CHF")
    st.write(f"Theorical amount with comission : {round(rate_currency_to_TAL(currency)*float(qty)*0.97,2)} TAL")
    
    
    st.markdown('---')
    sum -= 0.03*qty
    st.write(f'Amount with SQ fees and TAL comission : {round(rate_currency_to_TAL(currency)*sum,2)} TAL')

    fees_diff = (round(rate_currency_to_TAL(currency)*sum,2) - output_amount) / round(rate_currency_to_TAL(currency)*sum,2) *100    
    st.warning(f'Difference between theorical amount and final amount : {round(fees_diff,4)} % ')

    if st.checkbox('Show data'):
        st.dataframe(repartition)

with right_column:
    st.header('Exiting TAL')
    qty2 = st.number_input('Select quantity of TAL:', min_value=0, max_value=1000000000, value=1000, step=1000)
    currency2 = st.selectbox('Choose a currency in which you want to convert TAL:',  ['EUR','USD'] + list(currency_country_map.keys()))
    
    if qty2 == ""   :
        qty2 = 0

    data2 = pd.DataFrame({'TAL amount ': [qty2], 'Output amount ': [round(rate_TAL_to_currency(currency2)*float(qty2),2)], 'Output currency ': [currency2]})

    chf2 = qty2*100/1000
    eur2 = qty2*250/1000
    gbp2 = qty2*50/1000
    jpy2 = qty2*18000/1000
    cny2 = qty2*1600/1000
    sgd2 = qty2*80/1000
    usd2 = qty2*float(database.tail(1)['GLDUSD'] * 0.2)/1000
    gold2 = usd2/float(database.tail(1)['GLDUSD'])

    repartition2 = pd.DataFrame({'Currency': ['CHF', 'EUR', 'GBP', 'JPY', 'CNY', 'SGD', 'Gold oz'],
                            'Amount': [chf2, eur2, gbp2, jpy2, cny2, sgd2, gold2],
                            f'Amount in {currency2}': [conversion('CHF',currency2,chf2), conversion('EUR',currency2,eur2), conversion('GBP',currency2,gbp2), conversion('JPY',currency2,jpy2), conversion('CNY',currency2,cny2), conversion('SGD',currency2,sgd2), conversion('USD',currency2,usd2)],
                            'Fees':[conversion_with_fees('CHF',currency2,chf2)[0], conversion_with_fees('EUR',currency2,eur2)[0], conversion_with_fees('GBP',currency2,gbp2)[0], conversion_with_fees('JPY',currency2,jpy2)[0], conversion_with_fees('CNY',currency2,cny2)[0], conversion_with_fees('SGD',currency2,sgd2)[0], conversion_with_fees('USD',currency2,usd2)[0]],
                            f'Amount in {currency2} with fees':[conversion_with_fees('CHF',currency2,chf2)[1], conversion_with_fees('EUR',currency2,eur2)[1], conversion_with_fees('GBP',currency2,gbp2)[1], conversion_with_fees('JPY',currency2,jpy2)[1], conversion('CNY',currency2,cny2), conversion_with_fees('SGD',currency2,sgd2)[1], conversion_with_fees('USD',currency2,usd2)[1]]
    })
    sum2 = round(repartition2[f'Amount in {currency2} with fees'].sum(),2)
    
    st.markdown('*WITHOUT COMISSION*')

    st.write(f"Theorical amount : {round(rate_TAL_to_currency(currency2)*float(qty2),2)} {currency2}")
    st.write(f'Amount with fees : {sum2} {currency2}')

    st.markdown('---')

    st.markdown('*WITH COMISSION (0.5%)*')
    com = round(rate_TAL_to_currency(currency2),2)*(0.005*qty2)
    st.write(f"Theorical amount with comission : {round(rate_TAL_to_currency(currency2)*float(qty2),2)*0.97} {currency2}")
    st.write(f"Comission collected : {com} {currency2} or {conversion_with_fees(currency2,'CHF',com)[1]} CHF")
    
    
    st.markdown('---')
    sum2 -= com
    st.write(f'Amount with SQ fees and TAL comission : {sum2} {currency2}')

    fees_diff2 = (sum2 - round(rate_TAL_to_currency(currency2)*float(qty2),2)) / sum2 * 100    
    st.warning(f'Difference between theorical amount and final amount : {round(fees_diff2,4)} % ')
    if st.checkbox('Show data '):
        st.dataframe(repartition2)


st.markdown('---')

st.warning(f'**TOTAL FEES** : {round(fees_diff + fees_diff2),4} %')