import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import timedelta, datetime
import plotly.express as px
from plotly.graph_objs import *
import plotly.graph_objects as go
# If you are using EXCEL = import openpyxl

# from Insurance_claiming_forecasting.prediction import get_data,\
#     plot_future_forecast, plot_future_forecast_total, predict_col,\
#     predict_ind, predict_total, plot_predict_col, plot_predict_ind,\
#     plot_predict_total
from Insurance_claiming_forecasting import prediction

st.set_option('deprecation.showPyplotGlobalUse', False)


#Getting data
data_col, data_ind = prediction.get_data()

# Titles
st.markdown("""## **Welcome to the Prediction API**""")
st.markdown("Please, define the time period you want to predict.")

#EXCEL

# if (data_col.index[-1] + timedelta(days=1)).date() < (data_ind.index[-1] + timedelta(days=1)).date():
#     start_date = (data_col.index[-1] + timedelta(days=1)).date()
# else:
#     start_date = (data_ind.index[-1] + timedelta(days=1)).date()

#CSV

if ((datetime.strptime(data_col.index[-1], '%Y-%m-%d').date()) + timedelta(days=1)) < ((datetime.strptime(data_ind.index[-1], '%Y-%m-%d').date()) + timedelta(days=1)):
    start_date = ((datetime.strptime(data_col.index[-1], '%Y-%m-%d').date()) + timedelta(days=1))
else:
    start_date = ((datetime.strptime(data_ind.index[-1], '%Y-%m-%d').date()) + timedelta(days=1))


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

