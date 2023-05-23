import streamlit as st
import datapungi_fed as dpf
import pandas as pd
import datetime
import requests
import io
import yfinance as yf

st.set_page_config(layout="wide")

st.sidebar.markdown("# Home ")

st.markdown("<h1 style='text-align: center; color : lightblue;'> Value analysis tool </h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color : lightblue;'>  </h1>", unsafe_allow_html=True)

#st.image('https://imgur.com/a/nMyIfAo')
today = datetime.datetime.today().strftime('%Y-%m-%d')
start_date = '2010-01-01'
currency_country_map = {
            #"USD": "USA",  # United States Dollar
            #"EUR": "EUR",  # Euro (used by multiple European countries)
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
            "KRW": "KOR",  # South Korean Won
            "TRY": "TUR",  # Turkish Lira
            "RUB": "RUS",  # Russian Ruble
            "INR": "IND",  # Indian Rupee
            "BRL": "BRA",  # Brazilian Real
            "ZAR": "ZAF",  # South African Rand
            "NOK": "NOR",  # Norwegian Krone
            "KRW": "KOR",  # South Korean Won
            "PLN": "POL",  # Polish Zloty
            "ARS": "ARG",  # Argentine Peso
            # Add more currencies and country codes here
        }
@st.cache_data
def LoadFred():
    fred = dpf.data("4836c0505f939fde997bcff5d008211d")
    XXUS = ['CH','MX','JP','KO','CA','VZ','IN','BZ','SZ','SF','HK','NO','SD','SI']
    USXX = ['UK','NZ','AL']
        #JP = Japan / CH = China /UK = United Kingdom / MX = Mexico
        #KO = South Korea / BZ = Brazil / SZ = Switzerland / AL = Australia
        #SF = South Africa / HK = Hong Kong / NZ = New Zealand / SD = Sweden
        #VZ = Venezuela / IN = India / NO = Norway /SI = Singapore
    datafred = fred.series('DEXUSEU')
    for i in range(len(XXUS)):
            key = 'DEX'+XXUS[i]+'US'
            datafred = datafred.join(fred.series(key))
    for i in range(len(USXX)):
            key = 'DEXUS'+USXX[i]
            datafred = datafred.join(fred.series(key))
    datafred.columns = datafred.columns.str.replace('DEX', '')
    datafred = datafred.rename(columns={'USEU': 'EURUSD', 'CHUS': 'USDCNY', 'MXUS':'USDMXN','JPUS':'USDJPY','KOUS':'USDKRW',
                                            'CAUS':'USDCAD','HKUS':'USDHKD','INUS':'USDINR','UKUS':'USDGBP', 
                                            'AUUS':'USDAUD','NZUS':'USDNZD','SDUS':'USDSEK','NOUS':'USDNOK',
                                            'SIUS':'USDSGD','SZUS':'USDCHF','SFUS':'USDZAR','BZUS':'USDBRL',
                                            'USUK':'USDGBP','USNZ':'USDNZD','USAL':'USDAUD','VZUS':'USDVEF'})
    datafred['EURUSD'] = 1/datafred['EURUSD']

    return datafred

@st.cache_data
def url_builder(currency, start_date, end_date):
        
        # Building blocks for the URL
        entrypoint = 'https://sdw-wsrest.ecb.europa.eu/service/' # Using protocol 'https'
        resource = 'data'           # The resource for data queries is always'data'
        flowRef ='EXR'              # Dataflow describing the data that needs to be returned, exchange rates in this case
        key = f'D.{currency}.EUR.SP00.A'    # Defining the dimension values, explained below

        # https://sdw-wsrest.ecb.europa.eu/help/ for more information on the API

        # Define the parameters
        parameters = {
            'startPeriod':start_date,  # Start date of the time series
            'endPeriod': end_date     # End of the time series
        }
        url = entrypoint + resource + '/'+ flowRef + '/' + key
        return url, parameters

@st.cache_data
def LoadBCE():
    databce = pd.DataFrame()
    response = requests.get(url_builder('USD', start_date, today)[0], params=url_builder('USD', start_date, today)[1], headers={'Accept': 'text/csv'})
    df = pd.read_csv(io.StringIO(response.text))
    df['OBS_VALUE'].describe()
    databce = df.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)
    databce['TIME_PERIOD'] = pd.to_datetime(databce['TIME_PERIOD'])
    databce = databce.set_index('TIME_PERIOD')
    databce = databce.rename(columns={'OBS_VALUE': f'USDEUR'})

    for i in currency_country_map.keys():
            response = requests.get(url_builder(i, start_date, today)[0], params=url_builder(i,start_date, today)[1], headers={'Accept': 'text/csv'})
            df = pd.read_csv(io.StringIO(response.text))
            
            if 'TIME_PERIOD' not in df.columns:
                print(f"No data found for currency {i}. Skipping.")
                continue

            ts = df.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)
            ts['TIME_PERIOD'] = pd.to_datetime(ts['TIME_PERIOD'])
            ts = ts.set_index('TIME_PERIOD')
            ts = ts.rename(columns={'OBS_VALUE': f'EUR{i}'})
            databce = databce.join(ts, how='left')
    
    return databce

@st.cache_data
def CallDatabase():
    bce = LoadBCE()
    fred = LoadFred()
    database = bce.join(fred, how='left')
    database = database.fillna(method='ffill')

    datagld = yf.download('GC=F', start = start_date, end=today, progress=False)['Adj Close']

    database['GLDUSD'] = datagld

    database['TALUSD'] = (1/database['USDCHF'])*100 + (1/database['USDEUR'])*250 + (1/database['USDGBP'])*50 + (1/database['USDJPY'])*18000 + (1/database['USDCNY'])*1600 + (1/database['USDSGD']*80) + ((database['GLDUSD'])*0.2)

    database['TALUSD'] = database['TALUSD']*0.001

    database['TALEUR'] = (1/database['EURCHF'])*100 + 250 + (1/database['EURGBP'])*50 + (1/database['EURJPY'])*18000 + (1/database['EURCNY'])*1600 + (1/database['EURSGD']*80) + ((database['GLDUSD'])*0.2*(database['USDEUR']))

    database['TALEUR'] = database['TALEUR']*0.001

    database = database.fillna(method='ffill')

    return database

database = CallDatabase()

#st.dataframe(database[::-1])
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image('https://i.postimg.cc/g0JMMBbp/LOGO-TAL-AVEC-SIGNATURE.png')

