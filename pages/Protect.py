import streamlit as st
import plotly.graph_objects as go
import plotly_express as px
import pandas as pd
import requests
import json
from Home import database
from Home import currency_country_map

st.sidebar.markdown('# Protect with TAL')

st.title("Protect with TAL")

st.sidebar.image('https://i.postimg.cc/g0JMMBbp/LOGO-TAL-AVEC-SIGNATURE.png', use_column_width=True)

def conversion(from_currency, to_currency, amount):
    if from_currency == to_currency:
        return 1*amount
    amount = float(amount)
    
    url = f"https://www.boursorama.com/bourse/devises/convertisseur-devises/convertir?from={from_currency}%2F{currency_country_map.get(from_currency)}&to={to_currency}%2F[{currency_country_map.get(to_currency)}]&amount={amount}&showSpotLink=1"
    response = requests.get(url)
    response_text = response.text
    response_data = json.loads(response_text)
    #converted_amount = response_data["convertedAmount"]

    # Print the values
    #print("Converted Amount:", converted_amount)
    #print("Rate:", rate)
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
    # Add your content here
    currency = st.selectbox('Choose a currency to convert in TAL:', ['EUR','USD'] + list(currency_country_map.keys()))
    qty = st.number_input('Select quantity to protect :', min_value=0, max_value=1000000000, value=0, step=1000)
    #qty = float(st.text_input("Which amount", key="qty"))
    if qty == "":
        qty = 0
    output_amount = round(rate_currency_to_TAL(currency)*float(qty),2)
    st.write(f"You will receive = {output_amount} TAL")
    st.markdown('<body> <I> <p style="color:lightblue ";>This amount is without entry fees.</p></I></body>', unsafe_allow_html=True)
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
                            f'Amount in {currency}': [conversion('CHF',currency,chf), conversion('EUR',currency,eur), conversion('GBP',currency,gbp), conversion('JPY',currency,jpy), conversion('CNY',currency,cny), conversion('SGD',currency,sgd), conversion('USD',currency,usd)]})

    fig = px.pie(repartition, values=f'Amount in {currency}', names=[f"{row['Currency']} - {round(row['Amount'],2)}" for _, row in repartition.iterrows()], title='Basket Repartition at entry')#'Amount in {currency}'

    # Display the plot using Streamlit
    left_column.plotly_chart(fig, use_container_width=True)

    if st.checkbox('Show data'):   
        st.dataframe(data)
        st.dataframe(repartition)
    
    
# Add content to the right column
with right_column:
    st.header('Exiting TAL')
    # Add your content here
    qty2 = st.number_input('Select quantity of TAL:', min_value=0, max_value=1000000000, value=0, step=1000)
    currency2 = st.selectbox('Choose a currency in which you want to convert TAL:',  ['EUR','USD'] + list(currency_country_map.keys()))
    
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
   
    if st.checkbox('Show data  '):   
        st.dataframe(data2)
        st.dataframe(repartition2)   