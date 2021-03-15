import streamlit as st
import pandas as pd
import numpy as np
import plotly
from Insurance_claiming_forecasting import insurance
import plotly.express as px
import datetime

st.markdown("""# Welcome!""")

st.write('## This is your prediction interface')

d = st.date_input(
    "Choose the day to predict:",
    datetime.date(2019, 3, 1))

st.file_uploader('Select your file')

data = pd.read_excel('raw_data/full_data_clean.xlsx', engine='openpyxl')  ##REEMPLAZAR CSV FINAL

data_week = insurance.data_weekly(insurance.data_daily(data))


plot = st.radio('Select a plot', ('days', 'weeks', 'covid', 'otros'))

st.write(plot)

if plot == 'days':
    st.write('🔼')
elif plot == 'weeks':
    st.write('▶️')
elif plot == 'covid':
    st.write('🔽')
else:
    st.write('◀️')


st.line_chart(data_week)

fig = px.line(data_week, x='date_issue', y='total_amount_claims')
fig.show()
st.plotly_chart(fig)

