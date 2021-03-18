import pandas as pd
import numpy as np
import datetime

def get_clean_data(path):
    '''This function returns a Data Frame'''
    data = pd.read_excel(path, engine='openpyxl')
    data = data.drop(columns='SINIESTRO')
    data = data.drop_duplicates()
    '''Rename columns'''
    data = data.rename(columns={'ESTATUS': 'status',
                                'RAMOID': 'insurance_type',
                                'ENFERMEDAD': 'disease',
                                'TIPO_SIN':'claim_type',
                                'TP_PROVEEDOR': 'provider_type',
                                'ESTADO':'state',
                                'SEXO':'sex',
                                'EDAD':'age',
                                'CD_PAIS':'country_id',
                                'MONTO USD':'amount',
                                'FECHA CONTITUCION': 'date_issue',
                                'Rango Edad':'age_range',
                                'Hospitalizacion-Ambulatorio': 'h_type'
                                })
    '''Null values replace'''
    for col in data.columns[:5]:
        data[col] = data[col].fillna("No informado")
    data['state'] = data['state'].replace({'Estado No Identificado': 'Distrito Capital'})
    data['state'] = data['state'].fillna("Distrito Capital")
    data['sex'] = data['sex'].fillna("No informado")
    data['age'] = data['age'].fillna(data['age'].mean())
    data['country_id'] = data['country_id'].fillna(29)
    data['amount'] = data['amount'].fillna(0)
    data['date_issue'] = data['date_issue'].fillna(pd.to_datetime('1999-01-01'))
    for col in data.columns[11:]:
        data[col] = data[col].fillna("No informado")
    data['age_range'] = data['age_range'].replace({pd.to_datetime('2019-10-01 00:00:00'): 'No informado'})
    '''Split the data for data homogenization'''
    data = data.loc[(data['date_issue'] >= datetime.datetime(2018, 9, 1))]
    data.to_csv('data/clean_data.csv', index=False)
    return data

# Separate portfolio
def data_indiv(path):
    '''Regroup portfolio INDIVIDUAL'''
    data = get_clean_data(path)
    data_indiv = data.query('insurance_type == "INDIVIDUAL"')
    data_indiv = data_indiv.query('amount < 200000')
    return data_indiv

def data_colec(path):
    '''Regroup portfolio COLECTIVO'''
    data = get_clean_data(path)
    data_colec = data.query('insurance_type == "COLECTIVO"')
    data_colec = data_colec.query('amount < 60000')
    return data_colec

# Separate portfolio - daily
def data_indiv_daily(path):
    data = data_indiv(path)
    data_indiv_daily = data.groupby('date_issue', as_index = False).agg({'insurance_type': 'count', 'amount': 'sum'})
    data_indiv_daily.columns = ['date_issue','total_claims', 'total_amount_claims']
    return data_indiv_daily

def data_colec_daily(path):
    data = data_colec(path)
    data_colec_daily = data.groupby('date_issue', as_index = False).agg({'insurance_type': 'count', 'amount': 'sum'})
    data_colec_daily.columns = ['date_issue','total_claims', 'total_amount_claims']
    return data_colec_daily

# Separate frequency
def data_daily(path):
    '''Regroup data daily'''
    data = get_clean_data(path)
    data_days = data.groupby('date_issue', as_index = False).agg({'amount': 'sum'})
    data_days.columns = ['date_issue','total_amount_claims']
    return data_days

def data_weekly(path):
    '''Regroup data weekly'''
    data_days = data_daily(path)
    data_weeks = data_days.resample('W-Mon', on='date_issue').sum().reset_index().sort_values(by='date_issue')
    return data_weeks


# Separate frequency & covid_no-covid
def data_covid_daily(path):
    data = get_clean_data(path)
    data['covid_claims'] = data.disease.map(lambda x: 1 if 'Covid' in x else 0)
    data_covid_daily = data.groupby('date_issue', as_index = False).agg({'amount': 'sum', 'covid_claims': 'sum'})
    return data_covid_daily

def data_covid_weekly(path):
    data = get_clean_data(path)
    data_covid_days = data_covid_daily(path)
    data_covid_weekly = data_covid_days.resample('W-Mon', on='date_issue').sum().reset_index().sort_values(by='date_issue')
    return data_covid_weekly


# Separate portfolio & frequency & covid_no-covid
def data_indiv_covid_daily(path):
    '''Regroup data daily covid_no-covid'''
    data = data_indiv(path)
    data['covid_claims'] = data.disease.map(lambda x: 1 if 'Covid' in x else 0)
    data_indiv_covid_daily = data.groupby('date_issue', as_index = False).agg({'amount': 'sum', 'covid_claims': 'sum'})
    return data_indiv_covid_daily

def data_indiv_covid_weekly(path):
    '''Regroup data weekly covid_no-covid'''
    data_indiv_covid_days = data_indiv_covid_daily(path)
    data_indiv_covid_weekly = data_indiv_covid_days.resample('W-Mon', on='date_issue').sum().reset_index().sort_values(by='date_issue')
    return data_indiv_covid_weekly

def data_colec_covid_daily(path):
    '''Regroup data daily covid_no-covid'''
    data = data_colec(path)
    data['covid_claims'] = data.disease.map(lambda x: 1 if 'Covid' in x else 0)
    data_colec_covid_daily = data.groupby('date_issue', as_index = False).agg({'amount': 'sum', 'covid_claims': 'sum'})
    return data_colec_covid_daily

def data_colec_covid_weekly(path):
    '''Regroup data weekly covid_no-covid'''
    data_colec_covid_days = data_colec_covid_daily(path)
    data_colec_covid_weekly = data_colec_covid_days.resample('W-Mon', on='date_issue').sum().reset_index().sort_values(by='date_issue')
    return data_colec_covid_weekly


#funciones exclusivas de este scrip, cuando importe las funciones esto no corre
if __name__ == "__main__":
    path = '../data_heroku/data_siniestros.xlsx'
    print('hola')
    get_clean_data(path)
