# CHEQUEAR SI ESTO ES NECESARIO O CON EL REQUIREMENTS YA ES SUFICIENTE
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import xlsxwriter


class Insurance:

    def get_data(self):
        '''This function returns a Data Frame'''
        data = pd.read_excel('../raw_data/data_siniestros.xlsx', engine='openpyxl')
        return data

    def clean_data(self):
        data = data.drop(columns='SINIESTRO')
        data = data.drop_duplicates()
        return data

    def rename_columns(self):
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
        return data

    # EN REALIDAD EL DATA FRAME PUEDE VENIR CON OTROS VALORES VACIOS - VER ESTO
    def null_replace(self):
        data['state'].replace(np.nan, "Estado No Identificado", inplace=True)
        data['TP_PROVEEDOR'].replace(np.nan, "No Informado", inplace=True)
        return data

    def data_trim(self):
        data_trim = data.loc[(data['date_issue'] >= datetime(2018, 9, 1))]
        return data

    def data_daily(self):
        data_days = data.groupby('date_issue', as_index = False).agg({'amount': 'sum'})
        data_days.columns = ['date_issue','total_amount_claims']
        return data