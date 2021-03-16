import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import datetime
from datetime import timedelta
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

