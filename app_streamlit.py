import streamlit as st
import pandas as pd
import numpy as np
import plotly
from Insurance_claiming_forecasting import insurance
import plotly.express as px
import datetime
import base64
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import timedelta
from Insurance_claiming_forecasting import prediction



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
def get_cached_data_covid():
    cache_covid_data = insurance.data_covid_daily(path)
    return cache_covid_data
cache_covid = get_cached_data_covid()
@st.cache
def get_cached_data_daily():
    cache_data_daily = insurance.data_daily(path)
    return cache_data_daily
cache_daily = get_cached_data_daily()
@st.cache
def get_cached_data_indiv_daily():
    cache_data_indiv_daily = insurance.data_indiv_daily(path)
    return cache_data_indiv_daily
cache_indiv_daily = get_cached_data_indiv_daily()
@st.cache
def get_cached_data_colec_daily():
    cache_data_colec_daily = insurance.data_colec_daily(path)
    return cache_data_colec_daily
cache_colec_daily = get_cached_data_colec_daily()


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
    col1, col2, col3, col4 = st.beta_columns((8, 8, 10, 10))
    col1.markdown(f'''
    <div class="card text-white bg-info mb-3" style="width: 18rem">
        <div class="card-body">
            <h4 class="card-title">Total Claims</h4>
            <p class="card-text">{len(cache_data):,d}</p>
        </div>
    </div>''', unsafe_allow_html=True)
    col2.markdown(f'''
    <div class="card text-white bg-info mb-3" style="width: 18rem">
        <div class="card-body">
            <h4 class="card-title">Total Amount</h4>
            <p class="card-text">{sum(cache_data['amount']):,d}</p>
        </div>
    </div>''', unsafe_allow_html=True)
    col3.markdown(f'''
    <div class="card text-white bg-info mb-3" style="width: 18rem">
        <div class="card-body">
            <h4 class="card-title">Total Claims Covid</h4>
            <p class="card-text">{sum(cache_covid['covid_claims']):,d}</p>
        </div>
    </div>''', unsafe_allow_html=True)
    amount_covid = cache_covid.query('covid_claims>0')['amount'].sum()
    col4.markdown(f'''
    <div class="card text-white bg-info mb-3" style="width: 18rem">
        <div class="card-body">
            <h4 class="card-title">Total Amount Covid</h4>
            <p class="card-text">{amount_covid:,d}</p>
        </div>
    </div>''', unsafe_allow_html=True)

    # Plot
    fig = px.line(cache_daily, x='date_issue', y='total_amount_claims', title='Company overview')
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")])))
    fig.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
    st.plotly_chart(fig)

    # Some pie_charts
    
    col1, col2 = st.beta_columns((5, 5))

    df_plot_sex = cache_data.groupby('sex', as_index = False).agg({'insurance_type':'count'})
    df_plot_sex.columns = ['sex','total_claims']
    pie_plot_sex = px.pie(df_plot_sex, values=df_plot_sex['total_claims'], names=df_plot_sex['sex'], title='Separate claims for sex', color='sex', color_discrete_map={'M':'royalblue', 'F':'cyan',})
    pie_plot_sex.update_layout(width=400, height=400, autosize=False, template="seaborn",)
    pie_plot_sex.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
    pie_plot_sex.update_layout(legend_font_size=10)
    col1.plotly_chart(pie_plot_sex)
    
    df_plot_age = cache_data.groupby('age_range', as_index = False).agg({'insurance_type':'count'})
    df_plot_age.columns = ['age_range','total_claims']
    pie_plot_age = px.pie(df_plot_age, values=df_plot_age['total_claims'], names=df_plot_age['age_range'], title='Separate claims for age range')
    pie_plot_age.update_layout(width=400, height=400, autosize=False, template="seaborn",)
    pie_plot_age.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
    pie_plot_age.update_layout(legend_font_size=10)
    col2.plotly_chart(pie_plot_age)


    #---Expander---#
    with st.beta_expander('Claims by state'):
        state_amount_df = cache_data.groupby('state', as_index= True).agg({'amount':'sum'})\
        .sort_values(by='amount', ascending = False)
        state_amount_df.columns = ['total_amount_claims']
        st.table(state_amount_df)
        st.bar_chart(state_amount_df)

    # Portfolio selection
    text = 'Choose the performance portfolio from the pulldown'
    menu = ['Select portfolio', 'Individual portfolio', 'Colective portfolio']
    select = st.selectbox(text, menu)
    if select == 'Select portfolio':
        st.write('Please select an option')
       
    elif select == 'Individual portfolio':
        daily_indiv_plot = px.line(cache_indiv_daily, x='date_issue', y='total_claims')
        daily_indiv_plot.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
        st.plotly_chart(daily_indiv_plot)

        if st.checkbox('COVID claimings'):
            st.write("In this section we are viewing the claims corresponding to covid")
            data_indiv_covid = insurance.data_indiv_covid_daily(path)
            covid_indiv_plot = px.line(data_indiv_covid, x='date_issue', y='covid_claims')
            covid_indiv_plot.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
            st.plotly_chart(covid_indiv_plot)
    else:
        daily_colec_plot = px.line(cache_colec_daily, x='date_issue', y='total_claims')
        daily_colec_plot.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
        st.plotly_chart(daily_colec_plot)

        if st.checkbox('COVID claimings'):
            st.write("In this section we are viewing the claims corresponding to covid")
            data_colec_covid = insurance.data_colec_covid_daily(path)
            covid_colec_plot = px.line(data_colec_covid, x='date_issue', y='covid_claims')
            covid_colec_plot.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
            st.plotly_chart(covid_colec_plot)

else:
    st.subheader('Claiming forecasting')

    st.set_option('deprecation.showPyplotGlobalUse', False)

    #Getting data
    data_col, data_ind = prediction.get_data()

    # Titles
    st.markdown("""## **Welcome to the Prediction API**""")
    st.markdown("Please, define the time period you want to predict.")

    if (data_col.index[-1] + timedelta(days=1)).date() < (data_ind.index[-1] + timedelta(days=1)).date():
        start_date = (data_col.index[-1] + timedelta(days=1)).date()
    else:
        start_date = (data_ind.index[-1] + timedelta(days=1)).date()

    st.write(f'*Prediction period starts on: {start_date}*')
    # Getting date imput
    end_date = st.date_input("Prediction period ends on:", value=datetime.date(2021, 4, 8))

    # Date error for past dates
    if end_date <= start_date + timedelta(days=5):
        st.markdown(f'The date you entered is invalid. Please, enter a date after {start_date + timedelta(days=5)}.')
    else:

        # Plotting prediction for both carteras
        st.markdown(f"""### **Forecast for all carteras from {start_date} till {end_date}**""")

        st.pyplot(prediction.plot_predict_total(data_col, data_ind, end_date))

        #Adding predicted amounts
        predicted_sum_m_total, lower_sum_m_total, upper_sum_m_total = prediction.pred_sum_total(data_col, data_ind, end_date)

        st.write(f'The predicted amount sums {predicted_sum_m_total} Million USD.')

        st.write(f'The 95% Confidence Interval goes from {lower_sum_m_total} Million USD to {upper_sum_m_total} Million USD.')

        # Plotting prediction for cartera colectiva
        st.markdown(f"""### **Forecast for Cartera Colectiva from {start_date} till {end_date}**""")

        st.pyplot(prediction.plot_predict_col(data_col, end_date))

        #Adding predicted amounts
        predicted_sum_m_col, lower_sum_m_col, upper_sum_m_col = prediction.pred_sum_col(data_col, end_date)

        st.write(f'The predicted amount sums {predicted_sum_m_col} Million USD.')

        st.write(f'The 95% Confidence Interval goes from {lower_sum_m_col} Million USD to {upper_sum_m_col} Million USD.')

        # Plotting prediction for cartera individual
        st.markdown(f"""### **Forecast for Cartera Individual from {start_date} till {end_date}**""")

        st.pyplot(prediction.plot_predict_ind(data_ind, end_date))

        #Adding predicted amounts
        predicted_sum_m_ind, lower_sum_m_ind, upper_sum_m_ind = prediction.pred_sum_ind(data_ind, end_date)

        st.write(f'The predicted amount sums {predicted_sum_m_ind} Million USD.')

        st.write(f'The 95% Confidence Interval goes from {lower_sum_m_ind} Million USD to {upper_sum_m_ind} Million USD.')


