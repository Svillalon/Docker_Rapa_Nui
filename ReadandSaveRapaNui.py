#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 13:53:36 2021

@author: charlie opazo and sebastian villalon

Reading and saving Rapa Nui ozonesounding data. Except for removing negative values,
and strange values, no cleansing or resampling is applied to the data.

Read all sounding data and return one file in .csv with all soundings.

Generate one file .csv for to save info about ozone profiles validation

Data for the period 1995-2019 was downloaded from https://woudc.org/
This set corresponds to sounding data per launch in Eastern Island station


"""

# Import
import pandas as pd
import numpy as np
from glob import glob
import os
import csv
import chardet


def lecture(filename):
    """
    Read individual sounding file and return dataframe with:
        - datetime launch [datetime format]
        - geopotential height [m]
        - pressure [hPa]
        - temperature [°C]
        - relative humidity [%]
        - ozone partial pressure [mPa]
        - wind speed [m/s], if it is measured
        - wind direction [°], if it is measured

    Parameters
    ----------
    filename : str
        Path + filename soundig data.

    Returns
    -------
    dataframes : DataFramr
        Datraframe with sounding data.

    """
    
    # Buscar tipo de encode del archivo
    with open(filename, 'rb') as file:
        enc=chardet.detect(file.read())['encoding']

    
    # Buscar lineas a saltar del header para leer datos del archivo.
    # Tambien busca fecha y hora de lanzamiento del sondeo en el archivo
    with open(filename, 'r', encoding=enc) as file:
        reader = csv.reader(file, delimiter=',')
             
        iline = 0
        for row in reader:
            if row == []:
                pass
            elif row[0] == 'UTCOffset':
                date = next(reader)[1:3]
                fecha = date[0]
                hora = date[1]
                fechahora = date[0] + ' ' + hora
            elif row[0] == '#PROFILE' or row[0] == '#PROFILE ':
                iline += 2
                break
            iline += 1
    
    # Cargar mediciones del sonde en dateframe
    if fecha == '2008-7-5':
        # Excepcion para archivo del 2008-7-5, distinto encode y error en header
        rows = []
        rows.extend(range(iline))
        rows.extend(range(iline+1, iline+3))
        dataframes = pd.read_csv(filename, skiprows=rows, encoding=enc)
    else:
        dataframes = pd.read_csv(filename, skiprows=iline, na_values= ['///'])
    
    # Crear vector de tiempo, con el tiempo de lanzamiento para agregar index
    # a dateframes
    N = dataframes.shape
    time = []
    for i in range(N[0]):
        time.append(fechahora)
    time = pd.to_datetime(time)
        
    dataframes.index = time
    dataframes.index.rename('Datetime', inplace=True)
    
    # Renombrar columnas que estan mal ordenadas
    badfiles = ['2007', '2008']
    
    if fecha[0:4] in badfiles:
        dataframes.rename(columns={'WindSpeed' : 'GPHeight', 'WindDirection' : 'RelativeHumidity',
                                  'GPHeight' : 'WindSpeed', 'RelativeHumidity' : 'WindDirection'},
                          inplace=True)
    

    
    # Extraer variables a ocupar
    if 'WindSpeed' in dataframes.keys():
        # Si el archivo tiene mediciones de viento
        variables = ['GPHeight','Pressure', 'Temperature', 'RelativeHumidity',
                      'O3PartialPressure', 'WindSpeed', 'WindDirection']
    else:
        # Si el archivo no tiene mediciones de viento
        variables = ['GPHeight','Pressure', 'Temperature', 'RelativeHumidity',
                      'O3PartialPressure']
        
    dataframes = dataframes[variables]
    
    
    return dataframes    




# Get path
path = os.getcwd()# use your path

# Cargar los nombres de todos los archivos en las carpetas
filenames = []
for year in range(1995, 2020):
    fns = os.path.join(path, "Data", str(year), str(year)+"*.csv")
    filenames += glob(fns)


# cargar todos los datos de ozonosondas en mismo dateframe
dfold_aux = pd.DataFrame()
for filename in filenames:
    df = lecture(filename)
    dfold_aux = pd.concat([dfold_aux, df])

# Datetime de lanzamiento
dates_aux = dfold_aux.index.drop_duplicates()
dates_sort = dates_aux.sort_values()

# sort dataframe by launch datetime
dfold = pd.DataFrame()
for dat in dates_sort:
    dfold = pd.concat([dfold, dfold_aux.loc[dat]])
    
# remove negative values in O3PartialPressure
dfold.O3PartialPressure[dfold.O3PartialPressure<0] = np.nan

# Save all profiles in one file
out_allsondes = os.path.join(path, 'RapaNui_all_ozonesondes.csv')
dfold.to_csv(out_allsondes, sep=';')




# Generar archivo que guarda fechas de lanzamiento, con formato para indicar
# lanzamientos validos, comentarios y rangos de alturas a eliminar. Actualiza
# el archivo si existe y tiene nuevas fechas, y si ya tiene las fechas cargadas
# no modifica el archivo existente

# Datetime de lanzamiento
dates = dates_sort
# Genera dateframe para guardar datetimes en formato para validarlos
df_valid_new = pd.DataFrame(data={'Valid_O3':np.nan*np.zeros(len(dates)), 
                                  'Height_inf_O3' : np.nan*np.zeros(len(dates)), 
                                  'Height_sup_O3' : np.nan*np.zeros(len(dates)), 
                                  'Valid_T':np.nan*np.zeros(len(dates)), 
                                  'Height_inf_T' : np.nan*np.zeros(len(dates)), 
                                  'Height_sup_T' : np.nan*np.zeros(len(dates)), 
                                  'Valid_P':np.nan*np.zeros(len(dates)), 
                                  'Height_inf_P' : np.nan*np.zeros(len(dates)), 
                                  'Height_sup_P' : np.nan*np.zeros(len(dates)), 
                                  'Valid_RH':np.nan*np.zeros(len(dates)), 
                                  'Height_inf_RH' : np.nan*np.zeros(len(dates)), 
                                  'Height_sup_RH' : np.nan*np.zeros(len(dates)), 
                                  'Valid_V':np.nan*np.zeros(len(dates)), 
                                  'Height_inf_V' : np.nan*np.zeros(len(dates)), 
                                  'Height_sup_V' : np.nan*np.zeros(len(dates)), 
                                  'Comments' : np.nan*np.zeros(len(dates))}, 
                            index=dates)
# Filename
filename_df_valid = os.path.join(path, 'RapaNui_dates_valid.csv')
# Verifica si archivo existe o no
if os.path.isfile(filename_df_valid):
    df_valid_old = pd.read_csv(filename_df_valid, delimiter=';', index_col=0, 
                               parse_dates=True)
    if ~df_valid_new.index.equals(df_valid_old.index):
        df_valid = pd.concat([df_valid_old, df_valid_new])
        df_valid = df_valid.iloc[~df_valid.index.duplicated(keep='first')]
        df_valid.sort_index(inplace=True)
        df_valid.to_csv(filename_df_valid, sep=';')
else:
    df_valid_new.to_csv(filename_df_valid, sep=';')




# Generar archivo con fechas en formato %yy %mm %dd %HH %MM´ para utilizar en 
# codigo generador de trayectores
filename_datestr = os.path.join(path, 'RapaNui_DatesStr_hysplit.csv')
dates_str = pd.DataFrame(dates.strftime('%y %m %d %H %M'))
dates_str.to_csv(filename_datestr, header=False,index=False)
