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
                label='Information',
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
                label='Tab four',
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
                                    dcc.Markdown(dedent(f'''Ozone climatology for Rapa Nui. Island location and photograph of Motu Nui and Motu Iti as seen from Orongo on the Rano Kau volcano, 
                                                        around 280 meters above sea level. Looking southwest. Photograph 2003 by Macarena San Martín'''), 
                                                 style={'font-size':'8px', 'margin-left':'75px'}),
                                    html.H1("Map", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}), 
                                    dcc.Graph(figure=fig)], 
                                    
                                     style={'display': 'inline-block', 'float':'right', 'width': '50%'})
                                                 ])]
#################################################Informacion en Español#####################################                              
        elif Switch_Lang==True:
            return[
                html.Div([
                html.Div([html.H1("Rapa Nui (27.16S, 109.43W, 41m)", style={'margin-left':'50px','text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             dcc.Markdown(dedent(f'''
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
                
                Data Disclaimer: These data have been collected at Rapa Nui by the Chilean Weather Office (DMC) under the auspices of the Global Atmospheric Watch (GAW) Programme of the World Meteorological Organization (WMO).

                The data on this website are subject to revision and reprocessing. Check dates of creation to download the most current version.
    
                Contact the station principal investigator(s) for questions concerning data techniques and quality.
                
                '''), style={'margin-left':'60px'})] ,  
                style={'color': 'black', 'width':'50%','fontFamily': '"Times New Roman"'
                                                    ,'backgroundColor': '#f6f6f6', 'display': 'inline-block', 'margin-top':'50px', 'border-right': '2px solid #0668a1'}), 
                html.Div([
                                          html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo), 
                                   style={'height':'45%', 'width':'450px','margin-right':'75px' ,'margin-left':'75px', 'margin-top':'75px', 'border': '0px solid #0668a1', 'border-radius': '10px'}), 
                                    dcc.Markdown(dedent(f'''Ozone climatology for Rapa Nui. Island location and photograph of Motu Nui and Motu Iti as seen from Orongo on the Rano Kau volcano, 
                                                        around 280 meters above sea level. Looking southwest. Photograph 2003 by Macarena San Martín'''), 
                                                 style={'font-size':'8px', 'margin-left':'75px'}),
                                    html.H1("Mapa", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}), 
                                    dcc.Graph(figure=fig)],
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
            return [html.Div([html.H1("Lamsal", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                              
                dcc.Markdown(dedent(f'''
                Las tendencias lineales en estos compuestos se calcularon utilizando un modelo de regresión de Fourier según (Lamsal et al., 2015; Tiao et al., 1990) 
                para estimar las componentes estacionales y lineales en las observaciones de Ozono . 
                De acuerdo a (Lamsal et al., 2015), al suponer que la serie temporal de los valores medios mensuales en las observaciones de ozono en Tololo esta 
                compuesta por tres sub-componentes aditivos, podemos descomponer nuestra regresión como:
                    <p> &Omega; =  &alpha; (t) + bt + R(t)  </p>
                Donde (\u03A9) es la componente estacional dependiente del tiempo (t), (b) una componente de tendencia lineal y (R) un residuo o ruido. 
                Así se puede estimar la mayoría de las curvas para los contaminantes atmosféricos al definir \u03B1(t) como una serie de Fourier con 
                coeficientes n<sub>j<sub> y m<sub>j<sub> para una cantidad de datos j, como:  
                    
                Entonces dichas magnitudes representadas por la componente en la tendencia lineal (b) permitirán cuantificar la evolución en la concentraciones 
                de los contaminantes analizados. El error en la regresión es calculado según (Tiao et al., 1990), al cual es obtenido mediante una función 
                no lineal dependiente de la autocorrelación y el número total de datos.    
                
                '''), style={'margin-left':'60px'})
            ], style={'width':'50%', 'display':'inline-block', 'margin-top':'50px'}), 
                                    html.Div([
                html.H1("Artículos", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                dcc.Markdown(dedent(f'''
              Gallardo, L., HenríQuez, A., Thompson, A. M., Rondanelli, R., Carrasco, J., Orfanoz-Cheuquelaf, A., et al. (2016). The first twenty years (1994-2014) of ozone soundings from Rapa Nui (27°S, 109°W, 51m a.s.l.). Tellus, Ser. B Chem. Phys. Meteorol. 68, 29484. doi:10.3402/tellusb.v68.29484.
                '''), style={'margin-left':'60px'})
                ], style={'margin-top':'50px','display':'inline-block','float':'right' ,'width':'50%'})
                                    ]
        if Switch_Lang==True:        
            return [html.Div([html.H1("Lamsal", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                              
                dcc.Markdown(dedent(f'''
                Las tendencias lineales en estos compuestos se calcularon utilizando un modelo de regresión de Fourier según (Lamsal et al., 2015; Tiao et al., 1990) 
                para estimar las componentes estacionales y lineales en las observaciones de Ozono . 
                De acuerdo a (Lamsal et al., 2015), al suponer que la serie temporal de los valores medios mensuales en las observaciones de ozono en Tololo esta 
                compuesta por tres sub-componentes aditivos, podemos descomponer nuestra regresión como:
                    <p> &Omega; =  &alpha; (t) + bt + R(t)  </p>
                Donde (\u03A9) es la componente estacional dependiente del tiempo (t), (b) una componente de tendencia lineal y (R) un residuo o ruido. 
                Así se puede estimar la mayoría de las curvas para los contaminantes atmosféricos al definir \u03B1(t) como una serie de Fourier con 
                coeficientes n<sub>j<sub> y m<sub>j<sub> para una cantidad de datos j, como:  
                    
                Entonces dichas magnitudes representadas por la componente en la tendencia lineal (b) permitirán cuantificar la evolución en la concentraciones 
                de los contaminantes analizados. El error en la regresión es calculado según (Tiao et al., 1990), al cual es obtenido mediante una función 
                no lineal dependiente de la autocorrelación y el número total de datos.    
                
                '''), style={'margin-left':'60px'})
            ], style={'width':'50%', 'display':'inline-block', 'margin-top':'50px'}), 
                                    html.Div([
                html.H1("Artículos", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                dcc.Markdown(dedent(f'''
               Gallardo, L., HenríQuez, A., Thompson, A. M., Rondanelli, R., Carrasco, J., Orfanoz-Cheuquelaf, A., et al. (2016). The first twenty years (1994-2014) of ozone soundings from Rapa Nui (27°S, 109°W, 51m a.s.l.). Tellus, Ser. B Chem. Phys. Meteorol. 68, 29484. doi:10.3402/tellusb.v68.29484.
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