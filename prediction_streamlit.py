import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import datetime
from datetime import timedelta
from Insurance_claiming_forecasting.prediction import get_data,\
    plot_future_forecast, plot_future_forecast_total, predict_col,\
    predict_ind, predict_total, plot_predict_col, plot_predict_ind,\
    plot_predict_total



st.markdown("""Welcome to the Prediction API""")


st.markdown("Please, enter the date you want to predict")

end_date = st.date_input('Last day of prediction:', value=datetime.date(2021, 4, 8))

#Getting data
data_col, data_ind = get_data()

# Plotting prediction for cartera colectiva
st.markdown("""Forecast for Cartera Colectiva""")

plot_predict_col(data_col, end_date)

# Plotting prediction for cartera individual
st.markdown("""Forecast for Cartera Individual""")

plot_predict_ind(data_ind, end_date)

# Plotting prediction for both carteras
st.markdown("""Forecast for both carteras""")

plot_predict_total(data_col, data_ind, end_date)
