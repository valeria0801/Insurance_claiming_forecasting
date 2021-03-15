import streamlit as st
import pandas as pd
import numpy as np
import plotly
from Insurance_claiming_forecasting import insurance
import plotly.express as px
import datetime
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
# SIDE BAR
# Agregar logo
text = "Select which tool you want to use:"
menu = ["Home", "Business Intelligence", "Claiming forecasting"]
choise = st.sidebar.selectbox(text, menu)
# CARDS
st.markdown(f'''
<div class="card text-white bg-info mb-3" style="width: 18rem">
    <div class="card-body">
        <h2 class="card-title">Total claims</h2>
        <p class="card-text">{len(cache_data):,d}</p>
    </div>
</div>''', unsafe_allow_html=True)
st.markdown(f'''
<div class="card text-white bg-info mb-3" style="width: 18rem">
    <div class="card-body">
        <h2 class="card-title">Total amount</h2>
        <p class="card-text">{sum(cache_data['amount']):,d}</p>
    </div>
</div>''', unsafe_allow_html=True)
st.markdown(f'''
<div class="card text-white bg-info mb-3" style="width: 18rem">
    <div class="card-body">
        <h2 class="card-title">Total claims COVID</h2>
        <p class="card-text">{sum(cache_covid['covid_claims']):,d}</p>
    </div>
</div>''', unsafe_allow_html=True)
# amount_covid = [sum(cache_covid['amount']) if cache_covid['covid_claims'] > 0 for cache_covid['covid_claims']
amount_covid = cache_covid.query('covid_claims>0')['amount'].sum()
st.markdown(f'''
<div class="card text-white bg-info mb-3" style="width: 18rem">
    <div class="card-body">
        <h2 class="card-title">Total amount COVID</h2>
        <p class="card-text">{amount_covid:,d}</p>
    </div>
</div>''', unsafe_allow_html=True)
# Ver que ponemos en Home(pantalla principal)
if choise == "Home":
    st.write('# Welcome! This is a Business Intelligence and predictions web application for an OR our insurance company')
elif choise == "Business Intelligence":
    text = 'Choose the performance portfolio from the pulldown'
    menu = ['Individual portfolio', 'Colective portfolio']
    st.multiselect(text, menu)
    if st.checkbox('With COVID'):
        data_covid = insurance.data_indiv_covid_daily(path)
        fig = px.line(data_covid, x='date_issue', y='covid_claims')
        st.plotly_chart(fig)
    # if st.checkbox('Without COVID'):
    #     data = insurance.data_indiv_covid_daily(path)
    #     fig = px.line(data, x='date_issue', y='covid_claims')
    #     fig.show()
        # st.plotly_chart(fig)
# import plotly.express as px
# fruits = ["apples", "oranges", "bananas"]
# fig = px.line(x=fruits, y=[1,3,2], color=px.Constant("This year"),
#              labels=dict(x="Fruit", y="Amount", color="Time Period"))
# fig.add_bar(x=fruits, y=[2,1,3], name="Last year")
# fig.show()
# lot = st.radio('Select a plot', ('days', 'weeks', 'covid', 'otros'))
# st.write(plot)
# if plot == 'days':
#     st.write(':arrow_up_small:')
# elif plot == 'weeks':
#     st.write(':arrow_forward:')
# elif plot == 'covid':
#     st.write(':arrow_down_small:')
# else:
#     st.write(':arrow_backward:')
# st.write('## This is your prediction interface')
# d = st.date_input(
#     "Choose the day to predict:",
#     datetime.date(2019, 3, 1))
# st.file_uploader('Select your file')
# data = pd.read_excel('raw_data/full_data_clean.xlsx', engine='openpyxl')  ##REEMPLAZAR CSV FINAL
# data_week = insurance.data_weekly(insurance.data_daily(data))
# st.line_chart(data_week)

