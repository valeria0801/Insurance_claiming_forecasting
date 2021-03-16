import streamlit as st
import pandas as pd
import numpy as np
import plotly
from Insurance_claiming_forecasting import insurance
import plotly.express as px
import datetime
import base64


###-----Wallpaper Image Local-----###

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('wallpaper.jpg')

###-----Wallpaper Image URL-----###

# background_image = '''
# <style>
# body {
# background-image: url("https://thumbs.dreamstime.com/b/big-data-analytics-business-intelligence-bi-concept-busin-investor-analyzing-stock-market-report-financial-dashboard-117257664.jpg");
# background-size: cover;
# }
# </style>
# '''

# st.markdown(background_image, unsafe_allow_html=True)


###-----Data-----###

path = 'raw_data/data_siniestros.xlsx'

@st.cache
def get_cached_data():
    cache_clean_data = insurance.get_clean_data(path)
    return cache_clean_data
cache_data = get_cached_data()

@st.cache
def get_cached_covid_data():
    cache_covid_data = insurance.data_covid_daily(path)
    return cache_covid_data
cache_covid = get_cached_covid_data()

@st.cache
def get_cached_data_daily():
    cache_data_daily = insurance.data_daily(path)
    return cache_data_daily
cache_daily = get_cached_data_daily()

###-----Side Bar-----###

#---Select Tool---#
text = "Select which tool you want to use:"
menu = ["Home", "Business Intelligence", "Claiming forecasting"]
choise = st.sidebar.selectbox(text, menu)

if choise == "Home":
    st.subheader("Welcome! Let's get started")
    st.write("To access this private content you need to be authenticated")

    st.subheader("Login")
    username = st.text_input("User Name")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if password == '123':
            st.success("Logged In as {}".format(username))
        else:
            st.warning("Incorrect Username")

elif choise == "Business Intelligence":

    #---Cards---#

    col1, col2, col3, col4 = st.beta_columns((10, 11, 14, 1))

    col1.markdown(f'''
    <div class="card text-white bg-info mb-3" style="width: 18rem">
        <div class="card-body">
            <h2 class="card-title">Total Claims</h2>
            <p class="card-text">{len(cache_data):,d}</p>
        </div>
    </div>''', unsafe_allow_html=True)

    col2.markdown(f'''
    <div class="card text-white bg-info mb-3" style="width: 18rem">
        <div class="card-body">
            <h2 class="card-title">Total Amount</h2>
            <p class="card-text">{sum(cache_data['amount']):,d}</p>
        </div>
    </div>''', unsafe_allow_html=True)

    col3.markdown(f'''
    <div class="card text-white bg-info mb-3" style="width: 18rem">
        <div class="card-body">
            <h2 class="card-title">Total Claims Covid</h2>
            <p class="card-text">{sum(cache_covid['covid_claims']):,d}</p>
        </div>
    </div>''', unsafe_allow_html=True)

    amount_covid = cache_covid.query('covid_claims>0')['amount'].sum()
    col4.markdown(f'''
    <div class="card text-white bg-info mb-3" style="width: 18rem">
        <div class="card-body">
            <h2 class="card-title">Total Amount Covid</h2>
            <p class="card-text">{amount_covid:,d}</p>
        </div>
    </div>''', unsafe_allow_html=True)

    fig = px.line(cache_daily, x='date_issue', y='total_amount_claims', title='Time Series with Range Slider and Selectors')
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")])))
    st.plotly_chart(fig)

    # text = 'Choose the performance portfolio from the pulldown'
    # menu = ['Individual portfolio', 'Colective portfolio']
    # st.selectbox(text, menu)
    # if st.checkbox('With COVID'):
    #     data_covid = insurance.data_indiv_covid_daily(path)
    #     fig = px.line(data_covid, x='date_issue', y='covid_claims')
    #     st.plotly_chart(fig)

    # st.header('Company overview')

    #---Expander---#

    with st.beta_expander('Claims by state'):
        state_amount_df = cache_data.groupby('state', as_index= True).agg({'amount':'sum'})\
        .sort_values(by='amount', ascending = False)
        state_amount_df.columns = ['total_amount_claims']
        st.table(state_amount_df)
        st.bar_chart(state_amount_df)


else:
    st.subheader("Predictive Dashboard")




# col1, col2 = st.beta_columns(2)
# col1.subheader('Columnisation')
# col2.subheader('vale')


# # lot = st.radio('Select a plot', ('days', 'weeks', 'covid', 'otros'))
# # st.write(plot)
# # if plot == 'days':
# #     st.write(':arrow_up_small:')
# # elif plot == 'weeks':
# #     st.write(':arrow_forward:')
# # elif plot == 'covid':
# #     st.write(':arrow_down_small:')
# # else:
# #     st.write(':arrow_backward:')
# # st.write('## This is your prediction interface')
# # d = st.date_input(
# #     "Choose the day to predict:",
# #     datetime.date(2019, 3, 1))
# # st.file_uploader('Select your file')
# # data = pd.read_excel('raw_data/full_data_clean.xlsx', engine='openpyxl')  ##REEMPLAZAR CSV FINAL
# # data_week = insurance.data_weekly(insurance.data_daily(data))
# # st.line_chart(data_week)

