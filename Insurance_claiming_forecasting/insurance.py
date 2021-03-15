import pandas as pd
import numpy as np
import datetime

def get_data():
    '''This function returns a Data Frame'''
    data = pd.read_excel('../raw_data/data_siniestros.xlsx', engine='openpyxl')
    return data

def clean_data(data):
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
    for col in data.columns[:7]:
        data[col] = data[col].fillna("No informado")
    data['age'] = data['age'].fillna(data['age'].mean())
    data['country_id'] = data['country_id'].fillna(29)
    data['amount'] = data['amount'].fillna(0)
    data['date_issue'] = data['date_issue'].fillna(pd.to_datetime('1999-01-01'))
    for col in data.columns[11:]:
        data[col] = data[col].fillna("No informado")

    '''Split the data for data homogenization'''
    data = data.loc[(data['date_issue'] >= datetime.datetime(2018, 9, 1))]

    return data

def data_daily(data):
    data_days = data.groupby('date_issue', as_index = False).agg({'amount': 'sum'})
    data_days.columns = ['date_issue','total_amount_claims']
    return data_days

def data_weekly(data_days):
    data_weekly = data_days.resample('W-Mon', on='date_issue').sum().reset_index().sort_values(by='date_issue')
    return data_weekly

def data_indiv(data):
    data_indiv = data.query('insurance_type == "INDIVIDUAL"')
    data_indiv_homog = data_indiv.query('amount < 200000')
    return data_indiv_homog

def data_colec(data):
    data_colec = data.query('insurance_type == "COLECTIVO"')
    data_colec_homog = data_colec.query('amount < 60000')
    return data_colec_homog

