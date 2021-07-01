#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 20:49:03 2021

@author: sebastian
"""
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import geopandas as gpd
from dash.dependencies import Input, Output
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os as os
import numpy as np
import datetime
import base64
from datetime import date
from datetime import timedelta
from textwrap import dedent
from datetime import datetime as dt
from scipy.optimize import leastsq
from __toolsTrend import *
from __Anim import *
from __Trayect import *
from __Profiles import *
from __Climatology import*
from __TrendGraphs import *


orig = os.getcwd()
fn_ozonosondes = orig + '/' + 'RapaNui_all_clear.csv' 
fn_ozonosondes_10 = orig + '/' + 'Ozonosondes_quantile10.csv'
fn_ozonosondes_30 = orig + '/' + 'Ozonosondes_quantile30.csv'
fn_ozonosondes_mean = orig + '/' + 'Ozonosondes_mean.csv'
fn_ozonosondes_70 = orig + '/' + 'Ozonosondes_quantile70.csv'
fn_ozonosondes_90 = orig + '/' + 'Ozonosondes_quantile90.csv'
fn_table = orig + '/Table_content.csv'
fn_trayect = orig + '/' +"RapaNui_BackTrajectories.csv"

ozonosondes_data = pd.read_csv(fn_ozonosondes, index_col=0, delimiter=';',parse_dates=True)
ozonosondes_climatology_10= pd.read_csv(fn_ozonosondes_10, index_col=0)
ozonosondes_climatology_30= pd.read_csv(fn_ozonosondes_30, index_col=0)
ozonosondes_climatology_mean= pd.read_csv(fn_ozonosondes_mean, index_col=0)
ozonosondes_climatology_70= pd.read_csv(fn_ozonosondes_70, index_col=0)
ozonosondes_climatology_90= pd.read_csv(fn_ozonosondes_90, index_col=0)
df_trayect = pd.read_csv(fn_trayect, index_col=[0,1,2], delimiter=';', parse_dates=True)
table_data = pd.read_csv(fn_table)

ozonosondes_data = ozonosondes_data.replace(9000, np.nan)
ozonosondes_data = ozonosondes_data.replace(9000000, np.nan)


image_filename_cr2 = 'logo_footer110.png'
encoded_image_cr2 = base64.b64encode(open(image_filename_cr2, 'rb').read()).decode('ascii')
image_filename_DMC = 'logoDMC_140x154.png'
encoded_image_DMC = base64.b64encode(open(image_filename_DMC, 'rb').read()).decode('ascii')
image_filename_tololo = 'RapaNui.png'
encoded_image_tololo = base64.b64encode(open(image_filename_tololo, 'rb').read()).decode('ascii')
image_filename_cr2_celeste = 'cr2_celeste.png'
encoded_image_cr2_celeste = base64.b64encode(open(image_filename_cr2_celeste, 'rb').read()).decode('ascii')
image_filename_GWA = 'gaw_logo.png'
encoded_image_GWA = base64.b64encode(open(image_filename_GWA, 'rb').read()).decode('ascii')
image_filename_Rapa_Nui_Map = 'Easter-Island-Map.png'
encoded_image_Rapa_Nui_Map = base64.b64encode(open(image_filename_Rapa_Nui_Map, 'rb').read()).decode('ascii')
###############diccionario con fechas##########################################
df_year =  ozonosondes_data.iloc[~ozonosondes_data.index.year.duplicated(keep='first')].index.year
dates = {str(i):{str(j): ozonosondes_data[str(i)+'-'+str(j)][~ozonosondes_data[str(i)+'-'+str(j)].index.day.duplicated(keep='first')].index.day 
                 for j in ozonosondes_data[str(i)][~ozonosondes_data[str(i)].index.month.duplicated(keep='first')].index.month} for i in df_year}
dates_years = list(dates.keys())

###############################################################################
###################################Mapa
##############cosas del mapa

fig = go.Figure(go.Scattergeo(lat=[-27.16], lon=[-109.43]))
fig.update_geos(projection_type="orthographic", projection_rotation=dict(lon=-80, lat=-30), bgcolor='rgba(0,0,0,0)',
                lataxis_showgrid=True, lonaxis_showgrid=True
                
                  )
fig.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0}, 
                  plot_bgcolor='#f6f6f6',
            paper_bgcolor='#f6f6f6')






####### operaciones para descargas
title=[i for i in table_data.columns if i!='Download_url']
df_table=table_data.drop(['Download_url'], axis = 1)


df_table['Download'] = pd.Series(html.A(html.P(str(i)), href=str(j)) for i,j in zip(table_data['Download'], table_data['Download_url']))



########



#################################################################################
### -tabs prperties
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
}

tab_selected_style = {
    'borderTop': '#1766a0',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#1766a0',
    'color': 'white',
    'padding': '6px'
}
###
colors = {
    'background': 'white',
    'text': '#7FDBFF',
    'background_2': 'white',
    'background_3': 'cyan'

}

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
################################### Configuración Encabezado Página Web##############    
    html.Div([
        html.Div([html.H2("Rapa Nui Ozonosondes", style={'font-size':'18pt','color': 'white','font-family': 'Abel', 'font-weight': '200 !important', 'margin-top': '28px', 'margin-left':'10px'})], style={'position':'absolute','display': 'inline-block'}),
             html.A([       
             html.Img(src='data:image/png;base64,{}'.format(encoded_image_cr2), style={'height':'80px'})],href = 'http://www.cr2.cl/', style={'margin-left': '400px', 'position':'absolute'}),
             html.A([     
             html.Img(src='data:image/png;base64,{}'.format(encoded_image_DMC),style = {'height':'80px'})], href='http://www.meteochile.gob.cl/PortalDMC-web', style={'margin-left': '700px', 'position':'absolute'}),
             html.A([     
             html.Img(src='data:image/png;base64,{}'.format(encoded_image_GWA),style = {'height':'80px'})], href='https://www.wmo.int/gaw/', style={'margin-left': '900px', 'position':'absolute'}),
             html.Div([
                 html.H2("Language:" , style={'font-size':'15pt','color': 'white', 'margin-top': '30px'})], style={'margin-left': '1050px','display': 'inline-block', 'position':'absolute'}
                 )
            ,
            html.Div([
        daq.ToggleSwitch(
                    id='Switch_Lang',
                    className='SwicthLang',
                    value=True,
                    )], style={'backgroundColor':'#1766a0','margin-top':'30px','margin-left': '1150px','display': 'inline-block', 'position':'absolute'})
        
    ],
    style={'backgroundColor':'#1766a0', 'height':'80px'}),
#####################################################################################    
    html.Div(id='tabs-content', style={'backgroundcolor':'#f6f6f6'})
])
########################################Contenido Página Web#########################
@app.callback(Output('tabs-content', 'children'),
              Input('Switch_Lang', 'value'))
def Web_Language(Switch_Lang):
#####################################Versión en Ingles###############################    
    if Switch_Lang==False:
        return [html.Div([
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Presentation',
                value='tab-1',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Graphs',
                value='tab-2',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Download Data',
                value='tab-3', className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Methods',
                value='tab-4',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
        ]),
    html.Div(id='tabs-content-classes')
])]
#######################################Version en Español ##########################      
    if Switch_Lang==True:
        return [html.Div([
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Presentación',
                value='tab-1',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Gráficos',
                value='tab-2',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Descargar Datos',
                value='tab-3', className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Métodos',
                value='tab-4',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
        ]),
    html.Div(id='tabs-content-classes')
])]

@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'),
              Input('Switch_Lang', 'value'))
def render_content(tab, Switch_Lang):
################################################Tab 1###################################  
    if tab == 'tab-1':
        if Switch_Lang==False:
################################################ Informacion en Ingles##################            
            return [html.Div([
                html.Div([html.H1("Rapa Nui(27.16S, 109.43W, 41m)", style={'margin-left':'10px',
                                                                                     'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'})
                ,dcc.Markdown(dedent(f'''
                                     
                Rapa Nui (27ºS, 109ºW, 51 m a.s.l.) is influenced year-around by the eastern edge of the Pacific high resulting in to easterly and southeasterly boundary layer winds. Precipitation is generally convective in connection with the nearness of the South Pacific Convergence Zone (SPCZ). Precipitation also occurs in connection with mid-latitude disturbances and deep trough passages. Another prominent circulation feature affecting Rapa Nui is the subtropical jet stream (STJ), and its variability along the year. The main subsidence area associated with the subtropical high is located in between Rapa Nui and Western South America. Subsidence associated with the subtropical high peaks in summer, and it is suppressed in fall when the SPCZ reaches the island. Although weaker than in summer, subsidence also prevails in winter and spring. The STJ remains stationary over the island between fall and spring. A convective signature is found along the year, but it is particularly important in fall and winter. El Niño Southern Oscillation (ENSO) explains a significant part of the variability referred to above is linked to changes in atmospheric circulation due ENSO. The Pacific Decadal Oscillation (PDO) also affects weather and climate over Rapa Nui. 
                The seasonally averaged soundings indicate a fall minimum and a late spring maximum in ozone in the upper troposphere. The former occurs as the SPCZ approaches the island. The latter is suggestive of stratosphere-troposphere-exchange linked to the strength of the subtropical high and the nearness of the STJ in late winter and spring, allowing downward transport of stratospheric O3 present above 200 hPa. Occasionally, mid-latitude disturbances reach Rapa Nui inducing tropopause breaks and intrusions of stratospheric ozone. In the lower troposphere, extremes are found in summer and winter and they appear to be modulated by changes in insolation and static stability, showing larger ozone mixing ratios in winter than in summer. 
                Anthropogenic climate change, and the expansion of the Hadley cell is expected to affect the underlying dynamics that explain stratosphere-troposphere exchange affecting ozone profile. Also, there is evidence of increasing ozone trends near the surface that might be explained in part by the increase of anthropogenic activities on Rapa Nui. Hence, the remote location of Rapa Nui provides a unique and privileged position to observe global change, and to verify satellite borne measurements and modeling.

                Principal Investigators: Laura Gallardo, Carmen Vega        
                Emails: [lgallard@u.uchile.cl](mailto:lgallard@u.uchile.cl), [carmen.vega@dgac.gob.cl](mailto:carmen.vega@dgac.gob.cl)
                
                Data Site Manager: Francisca Muñoz, CR2 – Center for Climate and Resilience Research.            
                Email: [fmunoz@dgf.uchile.cl](mailto:fmunoz@dgf.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data scientist: Charlie Opazo, CR2 - Center for Climate and Resilence Research.          
                Email: [charlie.opazo@ug.uchile.cl](mailto:charlie.opazo@ug.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data scientist: Sebastian Villalón, CR2 - Center for Climate and Resilence Research.             
                Email: [sebastian.villalon@ug.uchile.cl](mailto:sebastian.villalon@ug.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data Disclaimer: These data have been collected at Rapa Nui by the Chilean Weather Office (DMC) under the auspices of the Global Atmospheric Watch (GAW) Programme of the World Meteorological Organization (WMO).
    
                The data on this website are subject to revision and reprocessing. Check dates of creation to download the most current version.
    
                Contact the station principal investigator(s) for questions concerning data techniques and quality.
                
                
                
                '''), style={'margin-left':'24px'})] ,  
                style={'color': 'black', 'width':'50%','fontFamily': '"Times New Roman"'
                                                    ,'backgroundColor': '#f6f6f6', 'display': 'inline-block', 'margin-top':'50px', 'border-right': '2px solid #0668a1'}), 
                html.Div([
                                          html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo), 
                                   style={'height':'45%', 'width':'450px','margin-right':'75px' ,'margin-left':'75px', 'margin-top':'75px', 'border': '0px solid #0668a1', 'border-radius': '10px'}), 
                                    dcc.Markdown(dedent(f'''
                                                        Ozone climatology for Rapa Nui. Island location and photograph of Motu Nui and Motu Iti as seen from Orongo on the Rano Kau volcano, 
                                                        
                                                        around 280 meters above sea level. Looking southwest. Photograph 2003 by Macarena San Martín'''), 
                                                 style={'font-size':'8px', 'margin-left':'75px'}),
                                    html.H1("Map", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}), 
                                    dcc.Graph(figure=fig) , 
                                    html.H1("Interactive map", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),                                     
                                     html.Img(src='data:image/png;base64,{}'.format(encoded_image_Rapa_Nui_Map), 
                                   style={'height':'45%', 'width':'450px','margin-right':'75px' ,'margin-left':'75px', 'margin-top':'75px', 'border': '0px solid #0668a1', 'border-radius': '10px'})], 
                                    
                                     style={'display': 'inline-block', 'float':'right', 'width': '50%'})
                                                 ], style={'backgroundColor': '#f6f6f6', 'height':'700px'})]
#################################################Informacion en Español#####################################                              
        elif Switch_Lang==True:
            return[
                html.Div([
                html.Div([html.H1("Rapa Nui (27.16S, 109.43W, 41m)", style={'margin-left':'50px','text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             dcc.Markdown(dedent(f'''
                                                 
                Rapa Nui (27ºS, 109ºW, 51 m s.n.m.) está influenciado durante todo el año por el borde oriental del Pacífico, lo que resulta en vientos de la capa límite del este y sureste. La precipitación es 
                generalmente convectiva en relación con la proximidad de la Zona de Convergencia del Pacífico Sur (SPCZ). La precipitación también ocurre en relación con perturbaciones de latitudes medias y pasajes 
                de vaguadas profundas. Otra característica de circulación prominente que afecta a Rapa Nui es la corriente en chorro subtropical (STJ) y su variabilidad a lo largo del año. El área de hundimiento principal 
                asociada con el alto subtropical se encuentra entre Rapa Nui y el oeste de América del Sur. Subsidencia asociada con los picos subtropicales altos en verano, y se suprime en otoño cuando la SPCZ llega a la isla. Aunque 
                más débil que en verano, el hundimiento también prevalece en invierno y primavera. El STJ permanece estacionario sobre la isla entre el otoño y la primavera. Se encuentra una firma convectiva a lo largo del año, pero es 
                particularmente importante en otoño e invierno. El Niño Oscilación del Sur (ENOS) explica que una parte significativa de la variabilidad mencionada anteriormente está vinculada a cambios en la circulación atmosférica debido 
                al ENOS. La Oscilación Decadal del Pacífico (DOP) también afecta el clima y el clima en Rapa Nui. Los sondeos promediados estacionalmente indican un mínimo de otoño y un máximo de finales de primavera en el ozono en la troposfera 
                superior. Lo primero ocurre cuando la SPCZ se acerca a la isla. Esto último sugiere un intercambio estratosfera-troposfera vinculado a la fuerza del alto subtropical y la proximidad del STJ a fines del invierno y la primavera, lo que 
                permite el transporte descendente del O3 estratosférico presente por encima de 200 hPa. Ocasionalmente, las perturbaciones de latitudes medias llegan a Rapa Nui provocando rupturas de la tropopausa e intrusiones de ozono estratosférico. 
                En la troposfera inferior, los extremos se encuentran en verano e invierno y parecen estar modulados por cambios en la insolación y la estabilidad estática, mostrando mayores proporciones de mezcla de ozono en invierno que en verano. 
                Se espera que el cambio climático antropogénico y la expansión de la célula de Hadley afecten la dinámica subyacente que explica el intercambio estratosfera-troposfera que afecta el perfil del ozono. Además, hay evidencia de tendencias 
                crecientes del ozono cerca de la superficie que podrían explicarse en parte por el aumento de las actividades antropogénicas en Rapa Nui. Por lo tanto, la ubicación remota de Rapa Nui proporciona una posición única y privilegiada para observar 
                el cambio global y verificar las mediciones y modelos satelitales.
                
                Investigadoras Principales: Laura Gallardo, Carmen Vega        
                Emails: [lgallard@u.uchile.cl](mailto:lgallard@u.uchile.cl), [carmen.vega@dgac.gob.cl](mailto:carmen.vega@dgac.gob.cl)
                
                Data Site Manager: Francisca Muñoz, CR2 – Centro de Ciencia del Clima y la Resiliencia.         
                Email: [fmunoz@dgf.uchile.cl](mailto:fmunoz@dgf.uchile.cl)
                
                Data scientist: Charlie Opazo, CR2 - Center for Climate and Resilence Research.          
                Email: [charlie.opazo@ug.uchile.cl](mailto:charlie.opazo@ug.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data scientist: Sebastian Villalón, CR2 - Center for Climate and Resilence Research.             
                Email: [sebastian.villalon@ug.uchile.cl](mailto:sebastian.villalon@ug.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Descargo de responsabilidad sobre los datos: estos datos han sido recopilados en Tololo por la Oficina Meteorológica de Chile (DMC) bajo los auspicios del Programa de Vigilancia Atmosférica Global (GAW) de la Organización Meteorológica Mundial (OMM).

                Los datos de este sitio web están sujetos a revisión y reprocesamiento. Consulta las fechas de creación para descargar la versión más actual.
    
                Comuníquese con el investigador principal de la estación si tiene preguntas sobre las técnicas y la calidad de los datos.

                '''), style={'margin-left':'60px'})] ,  
                style={'color': 'black', 'width':'50%','fontFamily': '"Times New Roman"'
                                                    ,'backgroundColor': '#f6f6f6', 'display': 'inline-block', 'margin-top':'50px', 'border-right': '2px solid #0668a1'}), 
                html.Div([
                                          html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo), 
                                   style={'height':'45%', 'width':'450px','margin-right':'75px' ,'margin-left':'75px', 'margin-top':'75px', 'border': '0px solid #0668a1', 'border-radius': '10px'}), 
                                    dcc.Markdown(dedent(f'''
                                                        Ozone climatology for Rapa Nui. Island location and photograph of Motu Nui and Motu Iti as seen from Orongo on the Rano Kau volcano, 
                                                        
                                                        around 280 meters above sea level. Looking southwest. Photograph 2003 by Macarena San Martín'''), 
                                                 style={'font-size':'8px', 'margin-left':'75px'}),
                                    html.H1("Mapa", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}), 
                                    dcc.Graph(figure=fig),
                                    html.H1("", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),                                     
                                     html.Img(src='data:image/png;base64,{}'.format(encoded_image_Rapa_Nui_Map), 
                                   style={'height':'45%', 'width':'450px','margin-right':'75px' ,'margin-left':'75px', 'margin-top':'75px', 'border': '0px solid #0668a1', 'border-radius': '10px'})],                                                  
                                     style={'display': 'inline-block', 'float':'right', 'width': '50%', 'backgroundColor': '#f6f6f6'})
                                          ], style={'backgroundColor': '#f6f6f6', 'height':'700px'})]
#####################################################################################
    elif tab == 'tab-2':
        if Switch_Lang==False:
                return [html.Div([                
    html.Div([html.H1("Vertical Profiles", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
                              html.Div([
    html.Label("Date:", style={'color': '#0668a1','font-size':'18px', 'position':'absolute'}), 
    html.Div([
        html.Div([
    dcc.Dropdown(id='dropdown_years_eng',style={'margin-top':'10px'}, options=[{'label':year,'value':year} for year in dates_years], placeholder="Año",value='1997')
    ], style={'width': '20%','margin-left':'5px', 'display': 'inline-block'}),
    html.Div([
    dcc.Dropdown(id='dropdown_months_eng', placeholder="Mes",value = '3')
    ], style={'width': '20%','margin-top':'10px', 'display': 'inline-block'}),
    html.Div([
    dcc.Dropdown(id='dropdown_days_eng', placeholder="Día",value='7')
    ], style={'width': '20%','margin-top':'10px', 'display': 'inline-block'})
    
        
    ], style= {'width': '50%','display':'inline-block', 'margin-left':'60px', 'margin-top':'-13px'})
    ]),
            
            dcc.Graph(id='Vertical_profile_graph', figure={"layout":{"height":400, "width":1080}})], style={'margin':'auto','margin-top':'10px','width':'1080px', 'height':'500px'}),
                
            html.Div([
                html.Div([
                html.H1("Climatology", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
                html.Div([ html.Label('Date Range:', style={'margin-right':'5px','color': '#0668a1','font-size':'18px'}),
            dcc.DatePickerRange(
                id='calendar_1',
                start_date=date(1997, 5, 3),
                end_date=date(2014,5,3)
                )], style={'margin-left':'20px'}),
                html.Div([
                    html.Label('Variable:', style={'margin-right':'5px','color': '#0668a1','font-size':'18px'}), 
                          html.Div([dbc.Container(
                        [dbc.RadioItems(
            options=[
                {"label": "Ozone", "value": "O3_ppbv"},
                {"label": "Temperature", "value": "Temp"},
                {"label": "Mixing Ratio", "value": "Mixing_Ratio"},
                {"label": "HR", "value": "RH"},
                {"label": "U", "value": "U"},
                {"label": "V", "value": "V"}
                
            ],
            id="radio_Climatology",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="O3_ppbv"
        ),
    ],
    className="p-3",
    )], style={'display':'inline-block'})
        ],  style={'display':'inline-block', 'margin-left':'20px'})
                ,dcc.Graph(id="Climatology")], style={'margin-left':'100px','margin-top':'20px','width':'525px','height':'650px', 'display': 'inline-block'}
                ),
                html.Div([
                html.H1("Ozone Profile Animations", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'})
            ,dcc.Graph(figure= AnimENG(ozonosondes_data, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA,
                                       ozonosondes_climatology_90, ozonosondes_climatology_70,
                       ozonosondes_climatology_30, ozonosondes_climatology_10, 
                       ozonosondes_climatology_mean))
            ], style={'margin-left':'5px','width':'525px','height':'650px', 'display': 'inline-block'})
                ], style={'height':'750px', 'display':'inline-block'}),
            html.Div([
            html.Div([html.H1('Trend', style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}), html.Label('Trend: ', style = {'color':'#0668a1'}), 
                      html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "Lamsal", "value": "Lamsal"},
                {"label": "EMD", "value": "EMD"},
                {"label": "Linear", "value": "Linear"},
                {"label": "ThielSen", "value":"ThielSen"},
                {"label": "STL", "value":"STL"}
                
            ],
            id="radio_trend",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="Lamsal"
        ),
    ],
    className="p-3",
)
    ], style={'display':'inline-block'}),
                html.Div([
                html.Label('Height [Km]: ', style={'color':'#0668a1'}),html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "1 [km]", "value": 1},
                {"label": "6 [km]", "value": 6},
                {"label": "15 [km]", "value": 15}
                
            ],
            id="radio_height",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value=1
        ),
    ],
    className="p-3",
)
    ], style={'display':'inline-block'}), dcc.Graph(id='Trend')
            ])          
            ],  style={'margin-left':'100px','width':'525px','height':'400px', 'display': 'inline-block'})
                
            , html.Div([ 
            html.H1('Air Parcel Trayectory', style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
            dcc.Graph(id='trayectory')
            ], style={'margin-left':'5px','margin-top':'20px','width':'525px','height':'400px', 'display': 'inline-block'})
            ])
            
            ], style={'backgroundColor':'#f6f6f6', 'height':'2000px'})
        ]    
        if Switch_Lang==True:
            return [
################################################GRafico Tendencia################                
    html.Div([                
    html.Div([html.H1("Perfiles Verticales", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
                              html.Div([
    html.Label("Fecha:", style={'color': '#0668a1','font-size':'18px', 'position':'absolute'}), 
    html.Div([
        html.Div([
    dcc.Dropdown(id='dropdown_years_esp',style={'margin-top':'10px'}, options=[{'label':year,'value':year} for year in dates_years], placeholder="Año",value='1997')
    ], style={'width': '20%','margin-left':'5px', 'display': 'inline-block'}),
    html.Div([
    dcc.Dropdown(id='dropdown_months_esp', placeholder="Mes",value = '3')
    ], style={'width': '20%','margin-top':'10px', 'display': 'inline-block'}),
    html.Div([
    dcc.Dropdown(id='dropdown_days_esp', placeholder="Día",value='7')
    ], style={'width': '20%','margin-top':'10px', 'display': 'inline-block'})
    
        
    ], style= {'width': '50%','display':'inline-block', 'margin-left':'60px', 'margin-top':'-13px'})
    ]),
            
            dcc.Graph(id='Perfil_vertical_graf', figure={"layout":{"height":400, "width":1080}})], style={'margin':'auto','margin-top':'10px','width':'1080px', 'height':'500px'}),
                
            html.Div([
                html.Div([
                html.H1("Climatología", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
                html.Div([ html.Label('Intervalo de Tiempo:', style={'margin-right':'5px','color': '#0668a1','font-size':'18px'}),
            dcc.DatePickerRange(
                id='calendario_1',
                start_date=date(1997, 5, 3),
                end_date=date(2014,5,3)
                )], style={'margin-left':'20px'}),
                html.Div([
                    html.Label('Variable:', style={'margin-right':'5px','color': '#0668a1','font-size':'18px'}), 
                          html.Div([dbc.Container(
                        [dbc.RadioItems(
            options=[
                {"label": "Ozono", "value": "O3_ppbv"},
                {"label": "Temperatura", "value": "Temp"},
                {"label": "Razón de Mezcla", "value": "Mixing_Ratio"},
                {"label": "HR", "value": "RH"},
                {"label": "U", "value": "U"},
                {"label": "V", "value": "V"}
                
            ],
            id="radio_Climatologia",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="O3_ppbv"
        ),
    ],
    className="p-3",
    )], style={'display':'inline-block'})
        ],  style={'display':'inline-block', 'margin-left':'20px'})
                ,dcc.Graph(id="Climatologia")], style={'margin-left':'100px','margin-top':'20px','width':'525px','height':'650px', 'display': 'inline-block'}
                ),
                html.Div([
                html.H1("Perfiles de Ozono Animados", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'})
            ,dcc.Graph(figure= AnimESP(ozonosondes_data, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA,
                                       ozonosondes_climatology_90, ozonosondes_climatology_70,
                       ozonosondes_climatology_30, ozonosondes_climatology_10, 
                       ozonosondes_climatology_mean))
            ], style={'margin-left':'5px','width':'525px','height':'650px', 'display': 'inline-block'})
                ], style={'height':'750px', 'display':'inline-block'}),
            html.Div([
            html.Div([html.H1('Tendencia', style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}), html.Label('Tendencia: ', style = {'color':'#0668a1'}), 
                      html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "Lamsal", "value": "Lamsal"},
                {"label": "EMD", "value": "EMD"},
                {"label": "Linear", "value": "Linear"},
                {"label": "ThielSen", "value":"ThielSen"},
                {"label": "STL", "value":"STL"}
                
            ],
            id="radio_tendencia",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="Lamsal"
        ),
    ],
    className="p-3",
)
    ], style={'display':'inline-block'}),
                html.Div([
                html.Label('Altura [Km]: ', style={'color':'#0668a1'}),html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "1 [km]", "value": 1},
                {"label": "6 [km]", "value": 6},
                {"label": "15 [km]", "value": 15}
                
            ],
            id="radio_altura",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value=1
        ),
    ],
    className="p-3",
)
    ], style={'display':'inline-block'}), dcc.Graph(id='Tendencia')
            ])          
            ],  style={'margin-left':'100px','width':'525px','height':'400px', 'display': 'inline-block'})
                
            , html.Div([ 
            html.H1('Trayectoria parcela de aire', style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
            dcc.Graph(id='trayectoria')
            ], style={'margin-left':'5px','margin-top':'20px','width':'525px','height':'400px', 'display': 'inline-block'})
            ])
            
            ], style={'backgroundColor':'#f6f6f6', 'height':'2000px'})
        ]
    elif tab == 'tab-3':
        if Switch_Lang== False:
            return html.Div([  dcc.Markdown(dedent(f'''
                               CITATION – If you use this dataset please acknowledge the Chilean Weather Office, and cite L. Gallardo, A. Henríquez, A. M. Thompson, R. Rondanelli, J. Carrasco, A. Orfanoz-Cheuquelaf and P. Velásquez, The first twenty years (1994-2014) of Ozone soundings from Rapa Nui (27°S, 109°W, 51m a.s.l.), Tellus B, 2016. (DOI: 10.3402/tellusb.v68.29484)                    
                                                   ''')),
               dbc.Table.from_dataframe(df_table, striped=True, bordered=True, hover=True)
            ], style={'padding':'100px'})
        elif Switch_Lang==True:
            return html.Div([
                dcc.Markdown(dedent(f'''
                CITATION – If you use this dataset please acknowledge the Chilean Weather Office, and cite L. Gallardo, A. Henríquez, A. M. Thompson, R. Rondanelli, J. Carrasco, A. Orfanoz-Cheuquelaf and P. Velásquez, The first twenty years (1994-2014) of Ozone soundings from Rapa Nui (27°S, 109°W, 51m a.s.l.), Tellus B, 2016. (DOI: 10.3402/tellusb.v68.29484)                                   
                                                   '''))
                ,
                dbc.Table.from_dataframe(df_table, striped=True, bordered=True, hover=True)
                ], style={'padding':'100px'})
    elif tab == 'tab-4':
        if Switch_Lang==False:
            return [html.Div([
                
                html.H1("Data", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
#                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
               dcc.Markdown(dedent(f''' 
                        The data shown in this platform corresponds to the set collected between August 1994 and 2019 by DMC consists of 294 soundings. These soundings provide information 
                        on ozone, air pressure, temperature, dew point, and relative humidity from the surface to the lower stratosphere (30-35 km). Since 1999, wind speed and direction were added 
                        to the collection. These data are available at World Ozone and Ultraviolet Radiation Data Centre (WOUDC, http://www.woudc.org/).
                        
                        The O3 sensor used is the so-called Electrochemical Concentration Cell (ECC). The measuring principle is based on the titration of ozone in a potassium iodide (KI) sensing 
                        solution. A Science Pump Corporation (SPC) type of ECC ozonesonde instrument is used at Rapa Nui. The sensing solution KI strength is 1%, with 100% buffer. The ECC sonde is 
                        launched with a Väisälä RS92 radiosonde. Between 1995 and 1997, an OS815N sensor was used, thereafter, a CCE64B was utilized.             '''), 
                
                style={'margin-left':'60px'}) ,
                
                html.H1("Quality assurance and quality control", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
#                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
               dcc.Markdown(dedent(f''' 
                                   We carried out a careful visual inspection of all soundings available. Each sounding was reviewed trying to identify anomalous values, instrument malfunctioning, 
                                   etc. We used concurrent standard meteorological soundings to support the inspection of ozone soundings. We only excluded soundings that seemed to us evidently anomalous. 
                                   The number of analyzed and selected soundings per year and season are shown in Table 1. Once the cleansing and review process was completed, we linearly interpolated all soundings every 100 m. 
                                   A few soundings (5) were only available for mandatory pressure levels in 2012.                '''), 
                
                style={'margin-left':'60px'}) ,
#                 html.H1("Back trajectories", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
# #                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
#                 dcc.Markdown(dedent(f'''
#                                     Not available                '''), 
                
#                  style={'margin-left':'60px'}) ,

                html.H1("Back trajectories", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
#                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
               dcc.Markdown(dedent(f'''
                We use reanalysis data sets from National Centers for Environmental Prediction/Atmospheric Research (NCEP/NCAR) to characterize the large-scale meteorological features affecting Rapa Nui. 
                We use three-dimensional (3-D) wind fields every six hours to calculate seven-day back trajectories for each ozone sonde.Trajectories were initialized at sounding launch time for 3 initial heights, 4, 8 and 12 km 
                above mean sea level. For this purpose, we apply the Hybrid Single Particle Lagrangian Integrated Trajectory (HYSPLIT) model.                 '''), 
                
                style={'margin-left':'60px'}),


                html.H1("Trends", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
#                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
               dcc.Markdown(dedent(f'''
                Trends were calculated using several methods found in the literature. These methods are summarized below:

                                                   
                **STL:**
                This method  (Cleveland et al. 1990) of decomposing signals uses Loess techniques to generate local smoother functions. Then by decoupling the seasonality and separating the noise obtaining a monotonic function for the trend. Cleveland et al. 1990 
               
                **EMD**
                In this method (Huang et al. 1998), the signal is decomposed as a superposition of local sums of oscillatory components called Intrinsic Mode Functions (IMF). The IMF modes added to a function without oscillatory components reconstruct the original signal. 
                
                **Lamsal-Fourier:**
                This method (Lamsal et al. 2015) uses a multilinear regression model based on harmonic functions (Fourier regression) to determine the components in the linear trends.                

                **Thiel Sen:**
                In the Theil-Sen method (Theil 1992, Sen 1960), multiple slopes are calculated to select the final slope as the median of all these
                '''), 
                
                style={'margin-left':'60px'})
                
                ], style={'width':'50%', 'display':'inline-block', 'margin-top':'50px'}), 
                                                                html.Div([
                html.H1("Paper Rapa Nui", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                dcc.Markdown(dedent(f'''

                Calderón, J. and Fuenzalida, H. 2014. Radiación ultravioleta en Isla de Pascua: factores climáticos y ozono total. Stratus 2, 8. Revista de la Dirección Meteorológica de Chile. ISSN 0719-4544

                Gallardo, L., Henríquez, A., Thompson, A. M., Rondanelli, R., Carrasco, J., Orfanoz-Cheuquelaf, A., et al. (2016). The first twenty years (1994-2014) of ozone soundings from Rapa Nui (27°S, 109°W, 51m a.s.l.). Tellus, Ser. B Chem. Phys. Meteorol. 68, 29484. doi:10.3402/tellusb.v68.29484.
                
                
               '''), style={'margin-left':'60px'}) ,
                
               html.H1("Paper Trend", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                dcc.Markdown(dedent(f'''

                Cleveland, R., Cleveland, W., of official, J.M.J., undefined 1990,
                1990. STL: A seasonal-trend decomposition. nniiem.ru URL: http:
                //www.nniiem.ru/file/news/2016/stl-statistical-model.pdf .
                                    
                Huang, N.E., Shen, Z., Long, S.R., Wu, M.C., Snin, H.H., Zheng, Q., Yen, N.C., Tung, C.C., Liu, H.H., 1998. The empirical mode decom- position and the Hubert spectrum for nonlinear and non-stationary time series analysis. Proceedings of the Royal Society A: Mathemat- ical, Physical and Engineering Sciences 454, 903–995. doi: 10.1098/rspa.1998.0193 .
                
                
                Lamsal, L.N., Duncan, B.N., Yoshida, Y., Krotkov, N.A., Pickering,K.E., Streets, D.G., Lu, Z., 2015. U.S. NO2 trends (2005–2013): EPA Air Quality System (AQS) data versus improved observations from the Ozone Monitoring Instrument (OMI). Atmospheric Environment 110, 130–143. URL: http://linkinghub.elsevier.com/re
                
                
                Sen, P.K., 1960. On Some Convergence Properties of U-Statistics. Calcutta Statistical Association Bulletin 10, 1–18. URL:https://journals.sagepub.com/doi/abs/10.1177/00
               '''), style={'margin-left':'60px'})
               
                ], style={'margin-top':'50px','display':'inline-block','float':'right' ,'width':'50%'})
                  
                                    ]
        if Switch_Lang==True:        
            return [html.Div([

                html.H1("Datos", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
#                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
               dcc.Markdown(dedent(f''' 
                        Los datos mostrados en esta plataforma corresponden al conjunto recolectado entre agosto de 1994 y 2019 por DMC compuesto por 294 sondeos de O3. Estos sondeos proporcionan información
                        sobre el ozono, la presión del aire, la temperatura, el punto de rocío y la humedad relativa desde la superficie hasta la estratosfera inferior (30-35 km). Desde 1999, se agregaron la velocidad y la dirección del viento
                        a la colección. Estos datos están disponibles en el Centro mundial de datos sobre el ozono y la radiación ultravioleta (WOUDC, http://www.woudc.org/).
                        
                        El sensor de O3 utilizado es la llamada celda de concentración electroquímica (ECC). El principio de medición se basa en la valoración del ozono en un sensor de yoduro de potasio (KI)
                        solución. En Rapa Nui se utiliza un instrumento de sonda de ozono ECC de Science Pump Corporation (SPC). La concentración de KI de la solución de detección es del 1%, con tampón al 100%. La sonda ECC es
                        lanzado con una radiosonda Väisälä RS92. Entre 1995 y 1997, se utilizó un sensor OS815N, a partir de entonces, se utilizó un CCE64B. '''),                
                style={'margin-left':'60px'}) ,
                
                html.H1("Control de calidad de datos", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
#                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
               dcc.Markdown(dedent(f''' 
                                    Nosotros realizamos una cuidadosa inspección visual de todos los sondeos disponibles. Cada sondeo fue revisado tratando de identificar valores anómalos, mal funcionamiento del instrumento,
                                    etc. Usamos sondeos meteorológicos estándar concurrentes para apoyar la inspección de sondeos de ozono. Solo excluimos los sondeos que nos parecían evidentemente anómalos.
                                    El número de sondeos analizados y seleccionados por año y temporada se muestra en la Tabla 1. Una vez que se completó el proceso de limpieza y revisión, interpolamos linealmente todos los sondeos cada 100 m.
                                    Algunos sondeos (5) solo estaban disponibles para niveles de presión obligatorios en 2012.             '''), 
                
                style={'margin-left':'60px'}) ,
#                 html.H1("Back trajectories", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
# #                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
#                 dcc.Markdown(dedent(f'''
#                                     Not available                '''), 
                
#                  style={'margin-left':'60px'}) ,

                html.H1("Seguimiento de trajectorias", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
#                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
               dcc.Markdown(dedent(f'''
                Utilizamos conjuntos de datos de reanálisis de los Centros Nacionales de Predicción Ambiental / Investigación Atmosférica (NCEP / NCAR) para caracterizar las características meteorológicas a gran escala que afectan a Rapa Nui.
                 Usamos campos de viento tridimensionales (3-D) cada seis horas para calcular las trayectorias de retroceso de siete días para cada sonda de ozono. Las trayectorias se inicializaron en el momento del lanzamiento del sondeo para 3 alturas iniciales, 4, 8 y 12 km.
                 sobre el nivel medio del mar. Para ello, aplicamos el modelo de Trayectoria Integrada Lagrangiana Híbrida de Partícula Única (HYSPLIT, por su sigla en ingles). '''), 

                style={'margin-left':'60px'}),

                html.H1("Tendencias", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
#                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
               dcc.Markdown(dedent(f'''
                Trends were calculated using several methods found in the literature. These methods are summarized below:

                                                   
                **STL:**
                This method  (Cleveland et al. 1990) of decomposing signals uses Loess techniques to generate local smoother functions. Then by decoupling the seasonality and separating the noise obtaining a monotonic function for the trend. Cleveland et al. 1990 
               
                **EMD**
                In this method (Huang et al. 1998), the signal is decomposed as a superposition of local sums of oscillatory components called Intrinsic Mode Functions (IMF). The IMF modes added to a function without oscillatory components reconstruct the original signal. 
                
                **Lamsal-Fourier:**
                This method (Lamsal et al. 2015) uses a multilinear regression model based on harmonic functions (Fourier regression) to determine the components in the linear trends.                

                **Thiel Sen:**
                In the Theil-Sen method (Theil 1992, Sen 1960), multiple slopes are calculated to select the final slope as the median of all these
                '''), 
                
                style={'margin-left':'60px'})
                
                ], style={'width':'50%', 'display':'inline-block', 'margin-top':'50px'}), 
                                                                html.Div([
                html.H1("Artículos Rapa Nui", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                dcc.Markdown(dedent(f'''

                Calderón, J. and Fuenzalida, H. 2014. Radiación ultravioleta en Isla de Pascua: factores climáticos y ozono total. Stratus 2, 8. Revista de la Dirección Meteorológica de Chile. ISSN 0719-4544

                Gallardo, L., Henríquez, A., Thompson, A. M., Rondanelli, R., Carrasco, J., Orfanoz-Cheuquelaf, A., et al. (2016). The first twenty years (1994-2014) of ozone soundings from Rapa Nui (27°S, 109°W, 51m a.s.l.). Tellus, Ser. B Chem. Phys. Meteorol. 68, 29484. doi:10.3402/tellusb.v68.29484.
                
                
               '''), style={'margin-left':'60px'}) ,
                
               html.H1("Artículos Tendencia", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                dcc.Markdown(dedent(f'''

                Cleveland, R., Cleveland, W., of official, J.M.J., undefined 1990,
                1990. STL: A seasonal-trend decomposition. nniiem.ru URL: http:
                //www.nniiem.ru/file/news/2016/stl-statistical-model.pdf .
                                    
                Huang, N.E., Shen, Z., Long, S.R., Wu, M.C., Snin, H.H., Zheng, Q., Yen, N.C., Tung, C.C., Liu, H.H., 1998. The empirical mode decom- position and the Hubert spectrum for nonlinear and non-stationary time series analysis. Proceedings of the Royal Society A: Mathemat- ical, Physical and Engineering Sciences 454, 903–995. doi: 10.1098/rspa.1998.0193 .
                
                
                Lamsal, L.N., Duncan, B.N., Yoshida, Y., Krotkov, N.A., Pickering,K.E., Streets, D.G., Lu, Z., 2015. U.S. NO2 trends (2005–2013): EPA Air Quality System (AQS) data versus improved observations from the Ozone Monitoring Instrument (OMI). Atmospheric Environment 110, 130–143. URL: http://linkinghub.elsevier.com/re
                
                
                Sen, P.K., 1960. On Some Convergence Properties of U-Statistics. Calcutta Statistical Association Bulletin 10, 1–18. URL:https://journals.sagepub.com/doi/abs/10.1177/00
               '''), style={'margin-left':'60px'})

                    
                ], style={'margin-top':'50px','display':'inline-block','float':'right' ,'width':'50%'})]                        
    
################################# dropdown dinamicos##########################
@app.callback(
    dash.dependencies.Output('dropdown_months_eng', 'options'),
    [dash.dependencies.Input('dropdown_years_eng', 'value')]
)
def update_date_dropdown(year):
    return [{'label': i, 'value': i} for i in list(dates[year].keys())]

@app.callback(
    dash.dependencies.Output('dropdown_days_eng', 'options'),
    [dash.dependencies.Input('dropdown_years_eng', 'value'),
     dash.dependencies.Input('dropdown_months_eng', 'value')]
)
def update_date_dropdown3(dropdown_years_eng, dropdown_months_eng):
    return [{'label': i, 'value': i} for i in dates[dropdown_years_eng][dropdown_months_eng]]

###############################################################################

#################################dynamic dropdown##########################
@app.callback(
    dash.dependencies.Output('dropdown_months_esp', 'options'),
    [dash.dependencies.Input('dropdown_years_esp', 'value')]
)
def update_date_dropdown(year):
    return [{'label': i, 'value': i} for i in list(dates[year].keys())]

@app.callback(
    dash.dependencies.Output('dropdown_days_esp', 'options'),
    [dash.dependencies.Input('dropdown_years_esp', 'value'),
     dash.dependencies.Input('dropdown_months_esp', 'value')]
)
def update_date_dropdown3(dropdown_years_esp, dropdown_months_esp):
    return [{'label': i, 'value': i} for i in dates[dropdown_years_esp][dropdown_months_esp]]

###############################################################################

############################ Vertical Profiles ###############################
@app.callback(
    Output('Vertical_profile_graph', 'figure'),
    [Input('dropdown_years_eng', 'value'),
     Input('dropdown_months_eng', 'value'),
     Input('dropdown_days_eng', 'value')
     ]
    
    )
def update_graph(dropdown_years_eng, dropdown_months_eng, dropdown_days_eng):
    fig = vertical_profiles(dropdown_years_eng, dropdown_months_eng, dropdown_days_eng,
                      ozonosondes_climatology_90, ozonosondes_climatology_70,
                       ozonosondes_climatology_30, ozonosondes_climatology_10, 
                       ozonosondes_climatology_mean, ozonosondes_data)   
    return fig 

############################ Perfiles Verticales###############################
@app.callback(
    Output('Perfil_vertical_graf', 'figure'),
    [Input('dropdown_years_esp', 'value'),
     Input('dropdown_months_esp', 'value'),
     Input('dropdown_days_esp', 'value')
     ]
    
    )
def update_graph(dropdown_years_esp, dropdown_months_esp, dropdown_days_esp):
    fig = periles_verticales(dropdown_years_esp, dropdown_months_esp, dropdown_days_esp,
                             ozonosondes_climatology_90, ozonosondes_climatology_70,
                       ozonosondes_climatology_30, ozonosondes_climatology_10, 
                       ozonosondes_climatology_mean, ozonosondes_data)  
   
    return fig
#######################################Climatologia###################### 
@app.callback(
    Output('Climatologia', 'figure'),
      [Input('calendario_1', 'start_date'),
      Input('calendario_1', 'end_date'),
      Input('radio_Climatologia', 'value')
      ])
def update_graph(start_date, end_date, radio_Climatologia):
 
    fig =  Climatologia(start_date, end_date, radio_Climatologia, ozonosondes_data, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)
    return fig 
# ################################Animation################################
# @app.callback(
#     Output('AnimENG', 'figure'))
      
# def update_graph(ozonosondes_data):
#     fig = AnimENG(ozonosondes_data)
#     return fig

# ################################Animacion################################
# @app.callback(
#     Output('AnimESP', 'figure'))
      
# def update_graph(ozonosondes_data):
#     fig = AnimESP(ozonosondes_data)
#     return fig

#######################################Climatologya###################### 
@app.callback(
    Output('Climatology', 'figure'),
      [Input('calendar_1', 'start_date'),
      Input('calendar_1', 'end_date'),
      Input('radio_Climatology','value')])
def update_graph(start_date, end_date, radio_Climatology):
 
    fig = Climatology(start_date, end_date, radio_Climatology, ozonosondes_data, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)
    return fig
#######################################################################
@app.callback(Output('Tendencia', 'figure'),
              Input('radio_tendencia', 'value'),
              Input('radio_altura', 'value'))
def update_graph(radio_tendencia, radio_altura):
        fig = tendencia(radio_tendencia, radio_altura, ozonosondes_data)
        return fig
    
#################################### Trend ##################################

@app.callback(Output('Trend', 'figure'),
              Input('radio_trend', 'value'),
              Input('radio_height', 'value'))
def update_graph(radio_trend, radio_height):
        fig = trend(radio_trend, radio_height, ozonosondes_data)
        return fig
    

####################################### Trend ##########################

@app.callback(
    Output('trayectory', 'figure'),
    [Input('dropdown_years_eng', 'value'),
     Input('dropdown_months_eng', 'value'),
     Input('dropdown_days_eng', 'value')
     ])
def update_graph(dropdown_years_eng, dropdown_months_eng, dropdown_days_eng):
    fig = Trayectory(df_trayect,int(dropdown_years_eng), int(dropdown_months_eng), int(dropdown_days_eng))
    return fig
####################################### Trayectoria ##########################

@app.callback(
    Output('trayectoria', 'figure'),
    [Input('dropdown_years_esp', 'value'),
     Input('dropdown_months_esp', 'value'),
     Input('dropdown_days_esp', 'value')
     ])
def update_graph(dropdown_years_esp, dropdown_months_esp, dropdown_days_esp):
    fig = Trayectoria(df_trayect,int(dropdown_years_esp), int(dropdown_months_esp), int(dropdown_days_esp))
    return fig

if __name__ == '__main__':
    app.run_server(debug=False,host='0.0.0.0', port = 8050)