import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import timedelta, datetime
import plotly.express as px
from plotly.graph_objs import *
import plotly.graph_objects as go

def get_data():
    # EXCEL
    # data_ind= pd.read_excel('data_heroku/weekly_data_clean_with_covid_ind.xlsx', engine='openpyxl').drop(columns= 'Unnamed: 0').set_index('date_issue')
    # data_col= pd.read_excel('data_heroku/weekly_data_clean_with_covid_col.xlsx', engine='openpyxl').drop(columns= 'Unnamed: 0').set_index('date_issue')

    #CSV
    data_ind= pd.read_csv('Insurance_claiming_forecasting/data/data_indiv_covid_weekly.csv').set_index('date_issue')
    data_col= pd.read_csv('Insurance_claiming_forecasting/data/data_colec_covid_weekly.csv').set_index('date_issue')

    return data_col, data_ind

def predict_col(data_col, end_date):
    # Build and train model
    best_sarima_full_data = SARIMAX(endog= data_col['amount'], order=(0, 1, 1),seasonal_order=(1, 1, 0, 52))
    best_sarima_full_data = best_sarima_full_data.fit()
    # Predict

    #EXCEL
    #future_prediction_full_data = best_sarima_full_data.get_prediction(start = data_col.index[-1] + timedelta(days=1), end = end_date, dynamic = True, full_results = True)

    #CSV
    future_prediction_full_data = best_sarima_full_data.get_prediction(start = ((datetime.strptime(data_col.index[-1], '%Y-%m-%d').date()) + timedelta(days=1)), end = end_date, dynamic = True, full_results = True)

    # Create results and confidence intervals
    future_predicted_amount_full_data = future_prediction_full_data.prediction_results.forecasts[0]
    future_predicted_amount_df_full_data_col = pd.DataFrame(future_predicted_amount_full_data, index=future_prediction_full_data.row_labels)
    future_pred_ci_full_data_col = future_prediction_full_data.conf_int(alpha=0.05)
    # Returning prediction and CI
    return future_predicted_amount_df_full_data_col, future_pred_ci_full_data_col

def predict_ind(data_ind, end_date):
    # Build and train model
    best_sarima_full_data = SARIMAX(endog= data_ind['amount'], order=(0, 1, 1),seasonal_order=(1, 1, 0, 52))
    best_sarima_full_data = best_sarima_full_data.fit()
    # Predict

    #EXCEL
    #future_prediction_full_data = best_sarima_full_data.get_prediction(start = data_ind.index[-1] + timedelta(days=1), end = end_date, dynamic = True, full_results = True)

    #CSV
    future_prediction_full_data = best_sarima_full_data.get_prediction(start = ((datetime.strptime(data_ind.index[-1], '%Y-%m-%d').date())+ timedelta(days=1)), end = end_date, dynamic = True, full_results = True)
    # Create results and confidence intervals
    future_predicted_amount_full_data = future_prediction_full_data.prediction_results.forecasts[0]
    future_predicted_amount_df_full_data_ind = pd.DataFrame(future_predicted_amount_full_data, index=future_prediction_full_data.row_labels)
    future_pred_ci_full_data_ind = future_prediction_full_data.conf_int(alpha=0.05)
    # Returning prediction and CI
    return future_predicted_amount_df_full_data_ind, future_pred_ci_full_data_ind

def predict_total(data_col, data_ind, end_date):
    future_predicted_amount_df_full_data_col, future_pred_ci_full_data_col = predict_col(data_col, end_date)
    future_predicted_amount_df_full_data_ind, future_pred_ci_full_data_ind = predict_ind(data_ind, end_date)

    merged_pred = future_predicted_amount_df_full_data_col.merge(future_predicted_amount_df_full_data_ind, right_index=True, left_index=True)
    merged_pred['total_pred']= merged_pred['0_x'] + merged_pred['0_y']
    merged_ci = future_pred_ci_full_data_col.merge(future_pred_ci_full_data_ind, right_index=True, left_index=True)
    merged_ci['total_lower_amount'] = merged_ci['lower amount_x'] + merged_ci['lower amount_y']
    merged_ci['total_upper_amount'] = merged_ci['upper amount_x'] + merged_ci['upper amount_y']
    return merged_pred, merged_ci

# Functions to make interactive plots 2: Final version

#TOTAL

def final_plot_total(data_col, data_ind, end_date):

    # Generating total Data

    merged_pred, merged_ci = predict_total(data_col, data_ind, end_date)
    total_df = data_col.merge(data_ind, right_index=True, left_index=True)
    total_df['total_amount']= total_df['amount_x'] + total_df['amount_y']
    total_df= pd.DataFrame(total_df['total_amount'])
    total_df= pd.concat([total_df, merged_pred['total_pred']])
    total_df = total_df.merge(merged_ci, how='left', left_index=True, right_index=True)
    total_df= total_df[['total_amount', 0, 'total_lower_amount', 'total_upper_amount']]
    total_df.fillna(value= '', inplace=True)
    total_df['predicted_amount']= total_df[0]
    total_df.drop(columns=0, inplace=True)
    total_df = total_df.rename(columns= {'total_amount':'Historical Data',
    'total_lower_amount':'Lower CI Limit',
    'total_upper_amount': 'Upper CI Limit',
    'predicted_amount': 'Forecast'})

    # Plotting Pred and CI area for Total data

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=total_df.index, y=total_df['Upper CI Limit'],
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='95% Confidence Interval',
    ))
    fig.add_trace(go.Scatter(
        x=total_df.index, y=total_df['Forecast'],
        fill= 'tonexty',
        line_color='rgb(65, 105, 225)',
        fillcolor='rgb(228, 241, 255)',
        name='Forecast',
    ))

    fig.add_trace(go.Scatter(
        x=total_df.index, y=total_df['Lower CI Limit'],
        fill='tonexty',
        fillcolor='rgb(228, 241, 255)',
        line_color='rgba(255,255,255,0)',
        name='95% Confidence Interval',
    ))

    fig.add_trace(go.Scatter(
        x=total_df.index, y=total_df['Historical Data'],
        line_color='gray',
        name='Historical Data',
    ))
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    fig.update_layout(width=1000)
    fig.update_layout(height=525)

    fig.update_xaxes(rangeslider_visible=True)

    # fig.show()
    return fig


# COL

def final_plot_col(data_col, end_date):

    #Getting data
    future_predicted_amount_df_full_data_col, future_pred_ci_full_data_col = predict_col(data_col, end_date)
    data_col= data_col.drop(columns='covid_claims')
    concat_df = pd.concat([data_col, future_predicted_amount_df_full_data_col])
    concat_df['predicted_amount']= concat_df[0]
    concat_df.drop(columns=0, inplace=True)
    concat_df.fillna(value= '', inplace=True)
    total_df = concat_df.merge(future_pred_ci_full_data_col, how='left', left_index=True, right_index=True)
    total_df.fillna(value= '', inplace=True)
    total_df = total_df.rename(columns={'amount':'Historical Data', 'predicted_amount':'Forecast', 'lower amount':'Lower CI Limit', 'upper amount': 'Upper CI Limit'})

    #Plotting

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=total_df.index, y=total_df['Upper CI Limit'],
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='95% Confidence Interval',
    ))
    fig.add_trace(go.Scatter(
        x=total_df.index, y=total_df['Forecast'],
        fill= 'tonexty',
        line_color='rgb(65, 105, 225)',
        fillcolor='rgb(228, 241, 255)',
        name='Forecast',
    ))

    fig.add_trace(go.Scatter(
        x=total_df.index, y=total_df['Lower CI Limit'],
        fill='tonexty',
        fillcolor='rgb(228, 241, 255)',
        line_color='rgba(255,255,255,0)',
        name='95% Confidence Interval',
    ))

    fig.add_trace(go.Scatter(
        x=total_df.index, y=total_df['Historical Data'],
        line_color='gray',
        name='Historical Data',
    ))
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    fig.update_layout(width=1000)
    fig.update_layout(height=525)

    fig.update_xaxes(rangeslider_visible=True)

    # fig.show()
    return fig


# IND

def final_plot_ind(data_ind, end_date):

    #Getting data
    future_predicted_amount_df_full_data_ind, future_pred_ci_full_data_ind = predict_ind(data_ind, end_date)
    data_ind= data_ind.drop(columns='covid_claims')
    concat_df = pd.concat([data_ind, future_predicted_amount_df_full_data_ind])
    concat_df['predicted_amount']= concat_df[0]
    concat_df.drop(columns=0, inplace=True)
    concat_df.fillna(value= '', inplace=True)
    total_df = concat_df.merge(future_pred_ci_full_data_ind, how='left', left_index=True, right_index=True)
    total_df.fillna(value= '', inplace=True)
    total_df = total_df.rename(columns={'amount':'Historical Data', 'predicted_amount':'Forecast', 'lower amount':'Lower CI Limit', 'upper amount': 'Upper CI Limit'})

    #Plotting

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=total_df.index, y=total_df['Upper CI Limit'],
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='95% Confidence Interval',
    ))
    fig.add_trace(go.Scatter(
        x=total_df.index, y=total_df['Forecast'],
        fill= 'tonexty',
        line_color='rgb(65, 105, 225)',
        fillcolor='rgb(228, 241, 255)',
        name='Forecast',
    ))

    fig.add_trace(go.Scatter(
        x=total_df.index, y=total_df['Lower CI Limit'],
        fill='tonexty',
        fillcolor='rgb(228, 241, 255)',
        line_color='rgba(255,255,255,0)',
        name='95% Confidence Interval',
    ))

    fig.add_trace(go.Scatter(
        x=total_df.index, y=total_df['Historical Data'],
        line_color='gray',
        name='Historical Data',
    ))
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    fig.update_layout(width=1000)
    fig.update_layout(height=525)

    fig.update_xaxes(rangeslider_visible=True)

    # fig.show()
    return fig


# Final function for summaries

def pred_summary(data_col, data_ind, end_date):
    future_predicted_amount_df_full_data_col, future_pred_ci_full_data_col = predict_col(data_col, end_date)
    predicted_sum_m_col = round(future_predicted_amount_df_full_data_col[0].sum()/1000000, 2)
    lower_sum_m_col = round(future_pred_ci_full_data_col['lower amount'].sum()/1000000, 2)
    upper_sum_m_col = round(future_pred_ci_full_data_col['upper amount'].sum()/1000000, 2)
    future_predicted_amount_df_full_data_ind, future_pred_ci_full_data_ind = predict_ind(data_ind, end_date)
    predicted_sum_m_ind = round(future_predicted_amount_df_full_data_ind[0].sum()/1000000, 2)
    lower_sum_m_ind = round(future_pred_ci_full_data_ind['lower amount'].sum()/1000000, 2)
    upper_sum_m_ind = round(future_pred_ci_full_data_ind['upper amount'].sum()/1000000, 2)
    predicted_sum_m_total = round(predicted_sum_m_col + predicted_sum_m_ind,2)
    lower_sum_m_total = round(lower_sum_m_col + lower_sum_m_ind, 2)
    upper_sum_m_total = round(upper_sum_m_col + upper_sum_m_ind, 2)
    return predicted_sum_m_col, lower_sum_m_col, upper_sum_m_col, predicted_sum_m_ind, lower_sum_m_ind, upper_sum_m_ind, predicted_sum_m_total, lower_sum_m_total, upper_sum_m_total
