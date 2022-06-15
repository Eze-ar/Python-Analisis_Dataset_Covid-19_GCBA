# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 11:04:56 2021

@author: Eze Angió
"""

import pandas as pd
from datetime import datetime

url = "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/salud/\
reporte-covid/dataset_reporte_covid_sitio_gobierno.csv"

#df = pd.read_csv(url)

#for Debug:
#print(df.head())
#print(df.tail())
#print(df.info())

#Con Pandas puedo hacer el parseo y transformación a fechas (objetos Datetime) 
#usando el parámetro parse_dates
#primero defino mi parser según el formato del dataset ('01APR2020:00:00:00')

mi_parse_dates = lambda f: datetime.strptime(f, "%d%b%Y:%H:%M:%S")  
#lamba se usa para definir funcioner anónimas
# %b mes abreviado en inglés 3 letras  

df = pd.read_csv(url, parse_dates=['FECHA'], date_parser=mi_parse_dates)
#print(type(df))

#con parse_dates le decimos qué columnas parsear la fecha
#date_parser recibe como parámetro mi función lambda (o anónima) que es la que
#realiza el parseo según el formato de entrada

#for Debug:
#print(df.head(2),'\n',df.info())

#ahora puedo obtener las fechas de inicio y fin de los datos del Dataset
#(y como objetos Timestamp):
fecha_inicio = df["FECHA"].min()
fecha_final = df["FECHA"].max()

#for Debug:
#print(fecha_inicio)
#print(fecha_final)
#print(type(fecha_inicio))

#paso a formato día/mes/AÑO
fecha_inicio_str = fecha_inicio.strftime('%d/%m/%Y')
#print(fecha_inicio_str)

fecha_final_str = fecha_final.strftime('%d/%m/%Y')
#print(fecha_final_str)

#print(f'Dataset Covid-19 GCBA entre {fecha_inicio_str} a {fecha_final_str}')

#los datos no están ordenados por fecha! entonces para sí ordenarlos:
df = df.sort_values(by='FECHA')
#print(df.head(2)) #coincide el primer valor con el presentado antes 1/7/2020

#for Debug:
#print(df['TIPO_DATO'].value_counts())
#print(df['SUBTIPO_DATO'].value_counts())

df = df[df['SUBTIPO_DATO'] == 'casos_confirmados_reportados_del_dia']

#separo las columnas que me interesan
df = df[['FECHA', 'TIPO_DATO', 'VALOR']]  #columnas en formato lista

#for Debug:
#print(df.head())

#ahora filtro por los TIPO_DATO que me interesan:
tipos_seleccionados = ['casos_no_residentes', 'casos_residentes']
df = df[df['TIPO_DATO'].isin(tipos_seleccionados)]
#tal como se vió en el ejercicio 8.7 Python- UNSaM

#trabajo con una copia:
df = df.copy()

#for Debug:
#print(df.head())

#Quiero pasar a un formato donde RESIDENTES y NO_RESIDENTES sean COLUMNAS
#y a mismma fecha según corresponda cada cual presente la cantidad de casos
#positivos que le es propia


df_r = df[df['TIPO_DATO'] == 'casos_residentes'] #dataframe de (+) RESIDENTES
df_nr = df[df['TIPO_DATO'] == 'casos_no_residentes'] #dataframe de (+) NO_RESIDENTES

df_r = df_r.rename(columns={'VALOR':'POSITIVOS_RESIDENTES'})
df_nr = df_nr.rename(columns={'VALOR':'POSITIVOS_NO_RESIDENTES'})

#for Debug:
#print(df_r.head())
#print(df_nr.head())

#elimino las columnas TIPO_DATO ya que no las preciso mas

df_r = df_r.drop(['TIPO_DATO'], axis=1)
df_nr = df_nr.drop(['TIPO_DATO'], axis=1)

#print(df_r.head())
#print(df_nr.head())

#Mezclo ambos df sabiendo que comparten el campo 'FECHA':
df = df_r.merge(df_nr, on='FECHA')

#print(df.head())
#print(df.info())

#defino la columna FECHA como DatetimeIndex ya que después lo
#precisaré al "resamplear" mensualmente
df = df.set_index('FECHA')
df.index = pd.to_datetime(df.index)

#aplico el método 'resample' para muestrear 'M'ensualmente
#el promedio (usando el método mean() )
df_mensual_promedio = df.resample('M').mean()

df_mensual_promedio.plot(kind='bar',stacked=False)
#
#lo anterior es lo mismo que hacer:
#df_mensual_promedio.plot.bar(rot=90)
#roto 90° las fechas para que no se solapen

#gráfico diario para este año:
df['2021-01-01':].plot()


#gráfico diario año 2020:
#df['2020-01-01':'2020-12-31'].plot()


print('Promedio mensual de casos Covid (+) detectacdos en CABA\n')
print(f'Rango: {fecha_inicio_str} a {fecha_final_str}')
print(df_mensual_promedio)
print('\nMaximos promedios mensuales', df_mensual_promedio.max())

