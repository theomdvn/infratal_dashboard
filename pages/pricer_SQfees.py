import streamlit as st
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
import plotly_express as px
import numpy as np
import requests
import json

MAJOR = ['EUR','USD','GBP','CHF','JPY','AUD','CAD','NZD']

MINOR = ['SEK','DKK','NOK','PNL','HKD']

EMERGING = ['THB','IRS','CZK','HUF','ILS','RUB','ISK','TRY','MXN','ZAR','SGD']
currency_country_map_SQ = {
            "JPY": "JPN",  # Japanese Yen
            "GBP": "GBR",  # British Pound Sterling
            "AUD": "AUS",  # Australian Dollar
            "CAD": "CAN",  # Canadian Dollar
            "CHF": "CHE",  # Swiss Franc
            "CNY": "CNH",  # Chinese Yuan
            "SEK": "SWE",  # Swedish Krona
            "NZD": "NIU",  # New Zealand Dollar
            "MXN": "MEX",  # Mexican Peso
            "SGD": "SGP",  # Singapore Dollar
            "HKD": "HKG",  # Hong Kong Dollar
            "NOK": "NOR",  # Norwegian Krone
            "TRY": "TUR",  # Turkish Lira
            "RUB": "RUS",  # Russian Ruble
            "BRL": "BRA",  # Brazilian Real
            "ZAR": "ZAF",  # South African Rand
            "NOK": "NOR",  # Norwegian Krone
            "PLN": "POL",  # Polish Zloty
            # Add more currencies and country codes here
        }

def fees_SQ(from_currency,to_currency,qty):
    if from_currency == to_currency:
        return 0
    elif from_currency in MAJOR and to_currency in MAJOR:
        if qty < 50000:
            return 0.0095
        elif qty < 100000:
            return 0.005
        elif qty < 250000:
            return 0.0038
        elif qty < 500000:
            return 0.0025
        else:
            return 0.0015
    elif (from_currency in MAJOR and to_currency in MINOR) or (from_currency in MINOR and to_currency in MAJOR):
        if qty < 50000:
            return 0.0125
        elif qty < 100000:
            return 0.01
        elif qty < 250000:
            return 0.005
        elif qty < 500000:
            return 0.0038
        else:
            return 0.0015
    elif (from_currency in MAJOR and to_currency in EMERGING) or (from_currency in EMERGING and to_currency in MAJOR):
        if qty < 50000:
            return 0.015
        elif qty < 100000:
            return 0.0125
        elif qty < 250000:
            return 0.01
        elif qty < 500000:
            return 0.006
        else:
            return 0.0015
    elif (from_currency in MINOR and to_currency in MINOR):
        if qty < 50000:
            return 0.015
        elif qty < 100000:
            return 0.0125
        elif qty < 250000:
            return 0.01
        elif qty < 500000:
            return 0.006
        else:
            return 0.0015
    elif (from_currency in MINOR and to_currency in EMERGING) or (from_currency in EMERGING and to_currency in MINOR):
        if qty < 50000:
            return 0.02
        elif qty < 100000:
            return 0.0175
        elif qty < 250000:
            return 0.015
        elif qty < 500000:
            return 0.0125
        else:
            return 0.005
    elif from_currency in EMERGING and to_currency in EMERGING:
        if qty < 50000:
            return 0.025
        elif qty < 100000:
            return 0.02
        elif qty < 250000:
            return 0.015
        elif qty < 500000:
            return 0.01
        else:
            return 0.003
    else: 
        return 0
        

from Home import database

st.sidebar.markdown('# Protect with TAL')

st.title("Protect with TAL")

st.sidebar.image('https://i.postimg.cc/g0JMMBbp/LOGO-TAL-AVEC-SIGNATURE.png', use_column_width=True)


def conversion(from_currency, to_currency, amount):
    if from_currency == to_currency:
        return 1*amount
    amount = float(amount)
    
    url = f"https://www.boursorama.com/bourse/devises/convertisseur-devises/convertir?from={from_currency}%2F{currency_country_map_SQ.get(from_currency)}&to={to_currency}%2F[{currency_country_map_SQ.get(to_currency)}]&amount={amount}&showSpotLink=1"
    response = requests.get(url)
    response_text = response.text
    response_data = json.loads(response_text)

    return round(float((response_data["convertedAmount"])),2)
def rate_TAL_to_currency(currency):
    goldamount_in_usd = float(database.tail(1)['GLDUSD'] * 0.2)
    #https://or.fr/api/spot-prices?metal=XAU&currency=EUR&weight_unit=oz&boundaries=1
    if currency == 'USD':
        rate = conversion('CHF',currency,100) + conversion('EUR',currency,250) + conversion('GBP',currency,50) + conversion('JPY',currency,18000) + conversion('CNY',currency,1600) + conversion('SGD',currency,80) + goldamount_in_usd
    else:
        rate = conversion('CHF',currency,100) + conversion('EUR',currency,250) + conversion('GBP',currency,50) + conversion('JPY',currency,18000) + conversion('CNY',currency,1600) + conversion('SGD',currency,80) + conversion('USD',currency,goldamount_in_usd)
    
    return float(rate*0.001) 

def rate_currency_to_TAL(currency):
    return float(1/rate_TAL_to_currency(currency))

#---------------------------------------------------------------------#

def conversion_fees_SQ(from_currency, to_currency, amount):
    if from_currency == to_currency:
        return 1*amount
    amount = float(amount)
    
    url = f"https://www.boursorama.com/bourse/devises/convertisseur-devises/convertir?from={from_currency}%2F{currency_country_map_SQ.get(from_currency)}&to={to_currency}%2F[{currency_country_map_SQ.get(to_currency)}]&amount={amount}&showSpotLink=1"
    response = requests.get(url)
    response_text = response.text
    response_data = json.loads(response_text)
    return round(float((response_data["convertedAmount"]))*(1 - float(fees_SQ(from_currency,to_currency,amount))),2)

left_column, right_column = st.columns(2)

left_column_width = 0.5
right_column_width = 0.5

# Set the column widths
left_column = left_column.container()
right_column = right_column.container()

# Apply custom CSS to adjust column width
left_column.markdown(f'<style>div.stButton > button {{ width: {left_column_width*100}% }}</style>', unsafe_allow_html=True)
right_column.markdown(f'<style>div.stButton > button {{ width: {right_column_width*100}% }}</style>', unsafe_allow_html=True)

# Add content to the left column
with left_column:
    left_column.header('Entering TAL')
    currency = st.selectbox('Choose a currency to convert in TAL:', ['EUR','USD'] + list(currency_country_map_SQ.keys()))
    qty = st.number_input('Select quantity to protect :', min_value=0, max_value=1000000000, value=0, step=1000)
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
                            'Fees':[fees_SQ('CHF',currency,chf), fees_SQ('EUR',currency,eur), fees_SQ('GBP',currency,gbp), fees_SQ('JPY',currency,jpy), fees_SQ('CNY',currency,cny), fees_SQ('SGD',currency,sgd), fees_SQ('USD',currency,usd)],
                            f'Amount in {currency} with fees':[conversion_fees_SQ('CHF',currency,chf), conversion_fees_SQ('EUR',currency,eur), conversion_fees_SQ('GBP',currency,gbp), conversion_fees_SQ('JPY',currency,jpy), conversion_fees_SQ('CNY',currency,cny), conversion_fees_SQ('SGD',currency,sgd), conversion_fees_SQ('USD',currency,usd)]})
    st.dataframe(repartition)
    sum = repartition[f'Amount in {currency} with fees'].sum()
    st.write(sum)
    
    st.write(f"Theorical amount without comission {output_amount} TAL")
    st.write(f'Amount with fees without comission = {round(rate_currency_to_TAL(currency)*sum,2)} TAL')

    st.markdown('---')

    st.write(f"Theorical amount with comission {round(rate_currency_to_TAL(currency)*float(qty)*0.97,2)} TAL")
    st.write(f"Comission collected : {0.03*qty} {currency} or {conversion_fees_SQ(currency,'CHF',0.03*qty)} CHF")
    
    st.markdown('---')
    sum -= 0.03*qty
    st.write(f'Amount with fees and comission = {round(rate_currency_to_TAL(currency)*sum,2)} TAL')

    fees_diff = (round(rate_currency_to_TAL(currency)*sum,2) - output_amount) / round(rate_currency_to_TAL(currency)*sum,2) *100    
    st.warning(f'Difference between theorical amount and final amount : {fees_diff}')


    
# Add content to the right column
with right_column:
    st.header('Exiting TAL')
    # Add your content here
    qty2 = st.number_input('Select quantity of TAL:', min_value=0, max_value=1000000000, value=0, step=1000)
    currency2 = st.selectbox('Choose a currency in which you want to convert TAL:',  ['EUR','USD'] + list(currency_country_map_SQ.keys()))
    
    if qty2 == ""   :
        qty2 = 0

    st.write(f"You will receive = {round(rate_TAL_to_currency(currency2)*float(qty2),4)} {currency2}")
    st.markdown('<body> <I> <p style="color:lightblue ";>This amount is without exit fees.</p></I></body>', unsafe_allow_html=True)


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
                            f'Amount in {currency2}': [conversion('CHF',currency2,chf2), conversion('EUR',currency2,eur2), conversion('GBP',currency2,gbp2), conversion('JPY',currency2,jpy2), conversion('CNY',currency2,cny2), conversion('SGD',currency2,sgd2), conversion('USD',currency2,usd2)]})

    # Plot the data in a pie chart
    fig2 = px.pie(repartition2, values=f'Amount in {currency2}', names=[f"{row['Currency']} - {round(row['Amount'],2)}" for _, row in repartition2.iterrows()], title='Basket Repartition before exit')


    right_column.plotly_chart(fig2, use_container_width=True)
   
    if st.checkbox('Show data'):   
        st.dataframe(data2)
        st.dataframe(repartition2)   