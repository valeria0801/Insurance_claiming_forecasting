import streamlit as st
import pandas as pd
import numpy as np
import plotly
from Insurance_claiming_forecasting import insurance, prediction
import plotly.express as px
import datetime
import base64
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import timedelta
import time
# df = pd.read_csv('data/clean_data.csv')
# st.write(df)
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
path = 'Insurance_claiming_forecasting/data/clean_data.csv'

# @st.cache
# def get_cached_data():
#     cache_clean_data = insurance.get_clean_data(path)
#     return cache_clean_data
# cache_data = get_cached_data()
cache_data = pd.read_csv(path)
# @st.cache
# def get_cached_data_covid():
#     cache_covid_data = insurance.data_covid_daily(path)
#     return cache_covid_data
# cache_covid = get_cached_data_covid()
cache_covid = pd.read_csv('Insurance_claiming_forecasting/data/data_covid_daily.csv')
# # @st.cache
# def get_cached_data_daily():
#     cache_data_daily = insurance.data_daily(path)
#     return cache_data_daily
# cache_daily = get_cached_data_daily()
cache_daily = pd.read_csv('Insurance_claiming_forecasting/data/data_days.csv')
# # @st.cache
# def get_cached_data_indiv_daily():
#     cache_data_indiv_daily = insurance.data_indiv_daily(path)
#     return cache_data_indiv_daily
# cache_indiv_daily = get_cached_data_indiv_daily()
cache_indiv_daily = pd.read_csv('Insurance_claiming_forecasting/data/data_indiv_daily.csv')
# # @st.cache
# def get_cached_data_colec_daily():
#     cache_data_colec_daily = insurance.data_colec_daily(path)
#     return cache_data_colec_daily
# cache_colec_daily = get_cached_data_colec_daily()
cache_colec_daily = pd.read_csv('Insurance_claiming_forecasting/data/data_colec_daily.csv')
# # @st.cache
# def get_cached_data_indiv_covid_daily():
#     cached_data_indiv_covid_daily = insurance.data_indiv_covid_daily(path)
#     return cached_data_indiv_covid_daily
# cache_indiv_covid_daily = get_cached_data_indiv_covid_daily()
cache_indiv_covid_daily = pd.read_csv('Insurance_claiming_forecasting/data/data_indiv_covid_daily.csv')
# # @st.cache
# def get_cached_data_colec_covid_daily():
#     cached_data_colec_covid_daily = insurance.data_colec_covid_daily(path)
#     return cached_data_colec_covid_daily
# cached_colec_covid_daily = get_cached_data_colec_covid_daily()
cache_colec_covid_daily = pd.read_csv('Insurance_claiming_forecasting/data/data_colec_covid_daily.csv')


#---Auxiliar DataFrame---#
df_aux = cache_data.copy()
df_aux['iscovid'] = df_aux['disease'].str.contains('Covid')
claims = df_aux.groupby('iscovid').count()
claims.index = ['Otros','Covid']
amounts = df_aux.groupby('iscovid').sum()
amounts.index = ['Otros','Covid']

#---------------------#

###-----Side Bar-----###
#---Select Tool---#
text = "Select which tool you want to use:"
menu = ["Home", "Business Intelligence", "Claiming forecasting"]
choise = st.sidebar.selectbox(text, menu)


if choise == "Home":
    st.markdown("<h1 style='text-align: center; font-size: 300%;'>Welcome!</h1>", unsafe_allow_html=True)
    st.subheader("Let's get started")
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


    #---Margins---#
    st.markdown(f"""
    <style>
    .reportview-container .main .block-container{{max-width: 1000px;}}
    </style>
    """,
    unsafe_allow_html=True,)

    #---Title---#
    st.markdown("<h1 style='text-align: center; font-size: 300%; margin: 0px 0px 100px 0px;'>Business Intelligence</h1>", unsafe_allow_html=True)

    #---Cards---#
    col1, col2, col3, col4 = st.beta_columns((10, 10, 10, 10))

    col1.markdown(f'''
    <div class="card text-white bg-info mb-3" style="width: 18rem">
        <div class="card-body">
            <h4 class="card-title" style='font-size: 110%;'>Total Claims</h4>
            <p class="card-text" style='font-size: 135%;'><b>{claims['amount'].sum():,d}</b></p>
        </div>
    </div>''', unsafe_allow_html=True)

    col2.markdown(f'''
    <div class="card text-white bg-info mb-3" style="width: 18rem;">
        <div class="card-body">
            <h4 class="card-title" style='font-size: 110%;'>Total Claims Covid</h4>
            <p class="card-text" style='font-size: 135%;'><b>{claims['amount'][1]:,d}</b></p>
        </div>
    </div>''', unsafe_allow_html=True)

    col3.markdown(f'''
    <div class="card text-white bg-info mb-3" style="width: 18rem">
        <div class="card-body">
            <h4 class="card-title" style='font-size: 110%;'>Total Amount</h4>
            <p class="card-text" style='font-size: 135%;'><b>{amounts['amount'].sum():,d}</b></p>
        </div>
    </div>''', unsafe_allow_html=True)

    col4.markdown(f'''
    <div class="card text-white bg-info mb-3" style="width: 18rem">
        <div class="card-body">
            <h4 class="card-title" style='font-size: 110%;'>Total Amount Covid</h4>
            <p class="card-text" style='font-size: 135%;'><b>{amounts['amount'][1]:,d}</b></p>
        </div>
    </div>''', unsafe_allow_html=True)


    #---Pie charts claims & amounts---#
    col1, col2 = st.beta_columns((20, 20))

    pie_plot_claims = px.pie(claims, values='amount', names=claims.index, color=claims.index, title='Total claims vs covid claims', color_discrete_map={'Covid':'darkblue', 'Otros':'royalblue',})
    pie_plot_claims.update_layout(width=400, height=400, title_x=0.5, title_yanchor='top',)
    pie_plot_claims.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
    col1.plotly_chart(pie_plot_claims)
#    pie_plot_claims.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=18, marker=dict(colors=claims.index, line=dict(color='#000000', width=2)))
    # fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0, 0, 0.2, 0])])
    # fig.show()

    pie_plot_amounts = px.pie(amounts, values='amount', names=amounts.index, color=amounts.index, title='Total amounts vs covid amounts', color_discrete_map={'Covid':'darkblue', 'Otros':'royalblue',})
    pie_plot_amounts.update_layout(width=400, height=400, title_x=0.5, title_yanchor='top',)
    pie_plot_amounts.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
#    pie_plot_amounts.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=18, marker=dict(colors=amounts.index, line=dict(color='#000000', width=2)))
    col2.plotly_chart(pie_plot_amounts)


    #---Total amount claims plot---#
    fig = px.line(cache_daily, x='date_issue', y='total_amount_claims', title='Company overview',)
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
    fig.update_layout(width=1000, height=500)
    fig['data'][0]['line']['color']="black"
    st.plotly_chart(fig)

    #---Some pie charts---#
    col1, col2 = st.beta_columns((5, 5))

    df_plot_sex = cache_data.groupby('sex', as_index = False).agg({'insurance_type':'count'})
    df_plot_sex.columns = ['sex','total_claims']
    pie_plot_sex = px.pie(df_plot_sex, values=df_plot_sex['total_claims'], names=df_plot_sex['sex'], title='Separate claims for sex', color='sex', color_discrete_map={'M':'darkblue', 'F':'royalblue',})
    pie_plot_sex.update_layout(width=400, height=400, title_x=0.5, title_yanchor='top',)
    pie_plot_sex.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
    pie_plot_sex.update_layout(legend_font_size=10)

#    pie_plot_sex.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20, marker=dict(colors='sex', line=dict(color='#000000', width=2)))
    col1.plotly_chart(pie_plot_sex)

    df_plot_age = cache_data.groupby('age_range', as_index = False).agg({'insurance_type':'count'})
    df_plot_age.columns = ['age_range','total_claims']
    pie_plot_age = px.pie(df_plot_age, values=df_plot_age['total_claims'], names=df_plot_age['age_range'], title='Separate claims for age range', color='age_range', color_discrete_map={'40-49':'rgb(3, 157, 252)', '50-59':'rgb(14, 132, 204)', '60-69': 'rgb(8, 100, 156)', '30-39': 'rgb(10, 72, 110)', 'Mayor a 70': 'darkblue', '0-9': 'royalblue', '20-29': 'rgb(119, 164, 242)', 'No informado': 'rgb(70, 132, 240)',})
    pie_plot_age.update_layout(width=500, height=400, title_x=0.5, title_yanchor='top',)
    pie_plot_age.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
    pie_plot_age.update_layout(legend_font_size=10)
#    pie_plot_age.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20, marker=dict(colors=age_range, line=dict(color='#000000', width=2)))
    col2.plotly_chart(pie_plot_age)

    #---Expanders---#
    with st.beta_expander('Claims amounts by state'):
        state_amount_df = cache_data.groupby('state', as_index= True).agg({'amount':'sum'})\
        .sort_values(by='amount', ascending = False)
        state_amount_df.columns = ['total_amount_claims']
        state_amount_df_rank = state_amount_df['total_amount_claims'][:10]
        st.table(state_amount_df_rank)
        bar_plot_state = px.bar(state_amount_df_rank)
        bar_plot_state.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
        bar_plot_state.update_layout(width=1000, height=500, showlegend=False)
        st.plotly_chart(bar_plot_state)

    #---Map for Claims by state---#

    data_geo = cache_data.groupby('state', as_index=False).agg({'insurance_type': 'count'})
    data_geo.columns = ['ESTADO', 'total_claims_state']
    data_geo['ESTADO'] = data_geo['ESTADO'].str.upper()
    data_geo['ID'] = [2,3,4,5,6,7,8,9,0,10,11,12,13,14,15,16,17,
                   18,19,20,21,22,23]
    data_geo['ID'] = data_geo['ID'].astype(str)

    data_geo['lat'] = [8.567404676772563,7.878238233915126,10.258720213275376,
                  8.61894586475427,8.126562318826902,10.159406133026875,
                  9.623429349400682,9.20174105540071,10.484435654212977,
                  11.069474022921652,9.96575806132416,10.125741665641938,
                  8.571299723405597,10.354125788585792,9.776306241818299,
                  10.939135402894177,9.059073585671939,10.650849962356101,
                  7.965417850740996,9.36784149927373,10.58188981291398,
                  10.484801951464496,10.261567855011007]

    data_geo['long'] = [-64.9594684895549,-67.46656917292137,-67.58765538009972,
                   -70.2355519527175,-63.58546158009323,-68.02866395827277,
                   -68.91984348825437,-61.93342649281256,-66.90920609084017,
                   -69.7280547454928,-67.47547242839347,-69.34472426084402,
                   -71.18067836271413,-66.92039424818014,-63.22717426928289,
                   -64.01581657735747,-69.2422779061641,-62.728453958575756,
                   -72.14453585456303,-70.42853311681279,-66.67576664578135,
                   -68.78629970556295,-72.48261768993409]



    # fig = px.scatter_geo(data_geo, lat="lat", lon="long",
    #                     size="total_claims_state", title="Total claims by state, Venezuela",
    #                     scope="south america"
    #                     )

    # fig.update_geos(
    # center=dict(lon=-67, lat=9),fitbounds="locations")
    # fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})

    # # lataxis_range=[-50,20], lonaxis_range=[0, 200])
    # st.plotly_chart(fig)


    fig = px.scatter_mapbox(data_geo, lat="lat", lon="long", color="total_claims_state", size="total_claims_state",
                      color_continuous_scale=px.colors.cyclical.IceFire, size_max=60,
                      mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(width=1000, height=525)
    st.plotly_chart(fig)

    # import json

    # json_venezuela = 'Estados_Venezuela.json'

    # fig=px.choropleth(data_geo,
    #              geojson=json_venezuela,
    #              featureidkey='properties.ST_NM',
    #              locations='ID',        #column in dataframe
    #               color='total_claims_state',  #dataframe
    #               color_continuous_scale='Inferno',
    #                title='Rape cases across the states' ,
    #                height=700
    #               )

    # fig = fig.update_geos(fitbounds="locations", visible=False)
    # st.plotly_chart(fig)





    with st.beta_expander('Claims amounts by disease'):
        disease_amount_df = cache_data.groupby('disease', as_index= True).agg({'amount':'sum'})\
        .sort_values(by='amount', ascending = False)
        disease_amount_df.columns = ['total_amount_claims']
        disease_amount_df_rank = disease_amount_df['total_amount_claims'][:10]
        st.table(disease_amount_df_rank)
        bar_plot_disease = px.bar(disease_amount_df_rank)
        bar_plot_disease.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
        bar_plot_disease.update_layout(width=1000, height=500, showlegend=False)
        st.plotly_chart(bar_plot_disease)

    #---Portfolio selection---#
    text = 'Choose the performance portfolio from the pulldown'
    menu = ['Select portfolio', 'Individual portfolio', 'Colective portfolio']
    select = st.selectbox(text, menu)
    if select == 'Select portfolio':
        st.write('Please select an option')

    elif select == 'Individual portfolio':
        daily_indiv_plot = px.line(cache_indiv_daily, x='date_issue', y='total_claims')
        daily_indiv_plot.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
        daily_indiv_plot.update_layout(width=1000, height=500)
        st.plotly_chart(daily_indiv_plot)

        if st.checkbox('COVID claimings'):
            st.write('In this section we are viewing the claims corresponding to covid')
            covid_indiv_plot = px.line(cache_indiv_covid_daily, x='date_issue', y='covid_claims')
            covid_indiv_plot.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
            covid_indiv_plot.update_layout(width=1000, height=500)
            st.plotly_chart(covid_indiv_plot)
    else:
        daily_colec_plot = px.line(cache_colec_daily, x='date_issue', y='total_claims')
        daily_colec_plot.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
        daily_colec_plot.update_layout(width=1000, height=500)
        st.plotly_chart(daily_colec_plot)

        if st.checkbox('COVID claimings'):
            st.write('In this section we are viewing the claims corresponding to covid')
            covid_colec_plot = px.line(cache_colec_covid_daily, x='date_issue', y='covid_claims')
            covid_colec_plot.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',})
            covid_colec_plot.update_layout(width=1000, height=500)
            st.plotly_chart(covid_colec_plot)

else:
    st.set_option('deprecation.showPyplotGlobalUse', False)

    #---Margins---#
    st.markdown(f"""
    <style>
    .reportview-container .main .block-container{{max-width: 1000px;}}
    </style>
    """,
    unsafe_allow_html=True,)


    #Getting data
    data_col, data_ind = prediction.get_data()


    # Titles
    st.markdown("<h1 style='text-align: center; font-size: 300%; margin: 0px 0px 100px 0px;'>Claiming forecasting</h1>", unsafe_allow_html=True)
    st.markdown("""## **Welcome to the Prediction API**""")
    st.markdown("Please, define the time period you want to predict.")

    if (data_col.index[-1] + timedelta(days=1)).date() < (data_ind.index[-1] + timedelta(days=1)).date():
        start_date = (data_col.index[-1] + timedelta(days=1)).date()
    else:
        start_date = (data_ind.index[-1] + timedelta(days=1)).date()


    # Getting prediction horizon choice

    def get_select_box_data():
        return pd.DataFrame({
            'first column': ['2 Weeks', '1 Month', '2 Months', '3 Months', '6 Months', '1 year']
            })

    df = get_select_box_data()

    option = st.selectbox('', df['first column'])

    def get_end_date(option):
        if option == '2 Weeks':
            end_date = start_date + timedelta(days=12)
        elif option == '1 Month':
            end_date = start_date + timedelta(days=29)
        elif option == '2 Months':
            end_date = start_date + timedelta(days=57)
        elif option == '3 Months':
            end_date = start_date + timedelta(days=92)
        elif option == '6 Months':
            end_date = start_date + timedelta(days=182)
        else:
            end_date = start_date + timedelta(days=365)
        return end_date

    end_date = get_end_date(option)
    st.write(f'The prediction will start on {start_date} and will end on {end_date}.')


    # Plotting prediction for both carteras
    st.markdown(f"""### **Total Portfolio amount forecast for {option}**""")

    st.plotly_chart(prediction.final_plot_total(data_col, data_ind, end_date))

    #Adding predicted amounts
    predicted_sum_m_col, lower_sum_m_col, upper_sum_m_col, predicted_sum_m_ind, lower_sum_m_ind, upper_sum_m_ind, predicted_sum_m_total, lower_sum_m_total, upper_sum_m_total = prediction.pred_summary(data_col, data_ind, end_date)

    st.write(f'The predicted amount sums {predicted_sum_m_total} Million USD.')

    st.write(f'The 95% Confidence Interval goes from {lower_sum_m_total} Million USD to {upper_sum_m_total} Million USD.')

    # Plotting prediction for cartera colectiva
    st.markdown(f"""### **Collective Portfolio amount forecast for {option}**""")

    st.plotly_chart(prediction.final_plot_col(data_col, end_date))

    #Adding predicted amounts

    st.write(f'The predicted amount sums {predicted_sum_m_col} Million USD.')

    st.write(f'The 95% Confidence Interval goes from {lower_sum_m_col} Million USD to {upper_sum_m_col} Million USD.')

    # Plotting prediction for cartera individual
    st.markdown(f"""### **Individual Portfolio amount forecast for {option}**""")

    st.plotly_chart(prediction.final_plot_ind(data_ind, end_date))

    #Adding predicted amounts


    st.write(f'The predicted amount sums {predicted_sum_m_ind} Million USD.')

    st.write(f'The 95% Confidence Interval goes from {lower_sum_m_ind} Million USD to {upper_sum_m_ind} Million USD.')
