#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 17:50:23 2021

@author: sebastian
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
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
import dash_bootstrap_components as dbc

orig = os.getcwd()
fn_ozonosondes = orig + '\\' + 'RapaNui_all_clear.csv' 
ozonosondes_data = pd.read_csv(fn_ozonosondes, index_col=0, parse_dates=True)
image_filename_top = '[www.cr2.cl][151]header_full.png'
encoded_image_top = base64.b64encode(open(image_filename_top, 'rb').read()).decode('ascii')
image_filename_bot = '[www.cr2.cl][151]header_back.png'
encoded_image_bot = base64.b64encode(open(image_filename_bot, 'rb').read()).decode('ascii')
image_filename_RapaNui = 'RapaNui.png'
encoded_image_RapaNui = base64.b64encode(open(image_filename_RapaNui, 'rb').read()).decode('ascii')

app = dash.Dash(__name__)
app.layout = html.Div([
    html.A([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image_top), 
             style={'height':'10%', 'width':'100%'})
    ], href='http://www.cr2.cl/'), 
    html.Label('Language: '), 
    html.Button('English', id='btn1', n_clicks=0, value='English'),
    dbc.Button('Espanish', id='btn2', n_clicks=0, active=True)
            , html.Div(id='tabs-content'), html.Br(id='Language')]) 
@app.callback(Output('tabs-content', 'children'),
              Output('Language','children'),
              Input('btn1', 'n_clicks'),
              Input('btn2', 'n_clicks'))
def render_content(btn1, btn2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn1' in changed_id or changed_id==".":
        return [html.Div([dcc.Markdown(dedent(f'''
                # **Tololo** (30.169 S, 70.804 W, 81m)
                Principal Investigator: Laura Gallardo, CR2 – Center for Climate and Resilience Research.
                
                Email: [lgallard@u.uchile.cl](mailto:lgallard@u.uchile.cl)
                
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data Site Manager: Francisca Muñoz, CR2 – Center for Climate and Resilience Research.
                
                Email: [fmunoz@dgf.uchile.cl](mailto:fmunoz@dgf.uchile.cl)
                
                Data Disclaimer: These data have been collected at Rapa Nui by the Chilean Weather Office (DMC) under the auspices of the Global Atmospheric Watch (GAW) Programme of the World Meteorological Organization (WMO).
    
                The data on this website are subject to revision and reprocessing. Check dates of creation to download the most current version.
    
                Contact the station principal investigator(s) for questions concerning data techniques and quality.
                
                
                
                '''))] ,  
                style={'color': 'black', 'width':'50%','fontFamily': '"Times New Roman"'
                                                    ,'backgroundColor': 'White', 'display': 'inline-block'}), 
                html.Div([
                                          html.Img(src='data:image/png;base64,{}'.format(encoded_image_RapaNui), 
                                   style={'height':'100%', 'width':'100%'})], 
                                    
                                     style={'display': 'inline-block', 'float':'right', 'width': '50%'}), 
      html.H1("Vertical Profiles", style={'text-align': 'center', 'color': '#0668a1','backgroundColor':'white'}),
      html.Div([ html.Label('Intervalo de Tiempo:'),
            dcc.DatePickerRange(
                id='calendar_1',
                start_date=date(2015, 4, 10),
                end_date=date(2019,11,15)
                )], style={'backgroundColor':'white'}),
      html.Div([html.Label('Vertical Estrucutre of:'), dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'O3 [ppbv]', 'value': 'O3_ppbv'},
            {'label': 'Temperature[K]', 'value': 'Temp'},
            {'label': 'RH', 'value':'RH'},
            {'label': 'O3 [mba]', 'value': 'O3_mba'},
            {'label': 'O3 [Du]', 'value': 'column'},
            {'label': 'U [m/s]', 'value': 'U'},
            {'label': 'V [m/s]', 'value': 'V'},
            {'label': 'O3 [ppbv]', 'value': 'O3_ppbv'},
            {'label': 'Theta [K]', 'value': 'Theta'},
            {'label': 'Theta e [K]', 'value': 'Theta_e'},
            {'label': 'Mixing Ratio [g/kg]', 'value': 'Mixing_Ratio'}
        ],
        value='O3_ppbv')], style={'widht':'15%'}
    ),dcc.Graph(id='fig1'),
      html.H1("Tencency line", style={'text-align': 'center', 'color': '#0668a1','backgroundColor':'white'}),
      html.Div([html.Label('Height [Km]:'), dcc.Input(id='input1', type="number",
    placeholder='Enter a value...',
    value=0.7)  

]),
        html.Div([html.Label('Tendency: '),
                  html.Button('Lamsal', id='btn-Lamsal', n_clicks=0),
                  html.Button('Carbone', id='btn-Carbone', n_clicks=0),
                  html.Button('Linear', id='btn-Linear', n_clicks=0)]),
        
        html.Div([dcc.Graph(id='Tendency_graph')]),              
        html.H1("Boxplot", style={'text-align': 'center','color': '#0668a1','backgroundColor':'White'})
     ,html.Div([html.Label('Height [Km]:'), dcc.Input(id='input2',
    placeholder='Enter a value...',
    type='number',
    value=5)  

])   
    ,html.Div([html.Label('Date Range:'),
            dcc.DatePickerRange(
                id='calendar_2',
                start_date=date(2015, 4, 10),
                end_date=date(2019,11,15)
                )], style={'backgroundColor':'white'}),
    dcc.Graph(id="boxplot1", style={'backgroundColor':'white'}), 
    html.H1("Histogram", style={'text-align': 'center','color': '#0668a1','backgroundColor':'White'}),
    html.Div([html.Label('Height [Km]:'), dcc.Input(id='input3',
    placeholder='Enter a value...',
    type='number',
    value=0.7)  

]),
    html.Div([html.Label('Date Range:'),
            dcc.DatePickerRange(
                id='calendar_3',
                start_date=date(2015, 4, 10),
                end_date=date(2019,11,15)
                )], style={'backgroundColor':'white'}),
    dcc.Graph(id="histogram", style={'backgroundColor':'white'}),
    html.Div([dcc.Markdown(dedent(f'''CITATION – If you use this dataset please acknowledge the Chilean Weather Office, and cite L. Gallardo, A. Henríquez, A. M. Thompson, R. Rondanelli, J. Carrasco, A. Orfanoz-Cheuquelaf and P. Velásquez, The first twenty years (1994-2014) of Ozone soundings from Rapa Nui (27°S, 109°W, 51m a.s.l.), Tellus B, 2016. (DOI: 10.3402/tellusb.v68.29484)

View in Tellus'''))]),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image_bot), 
              style={'height':'10%', 'width':'100%'})
], 'English'
    elif 'btn2' in changed_id:
       return [html.Div([dcc.Markdown(dedent(f'''
                # **Tololo** (30.169 S, 70.804 W, 81m)
                Principal Investigador: Laura Gallardo, CR2 – Centro de Ciencia del Clima y la Resiliencia.
                
                Email: [lgallard@u.uchile.cl](mailto:lgallard@u.uchile.cl)
                
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data Site Manager: Francisca Muñoz, CR2 – Centro de Ciencia del Clima y la Resiliencia.
                
                Email: [fmunoz@dgf.uchile.cl](mailto:fmunoz@dgf.uchile.cl)
                
                Data Disclaimer: These data have been collected at Rapa Nui by the Chilean Weather Office (DMC) under the auspices of the Global Atmospheric Watch (GAW) Programme of the World Meteorological Organization (WMO).
    
                The data on this website are subject to revision and reprocessing. Check dates of creation to download the most current version.
    
                Contact the station principal investigator(s) for questions concerning data techniques and quality.
                
                '''))] ,  
                style={'color': 'black', 'width':'50%','fontFamily': '"Times New Roman"'
                                                    ,'backgroundColor': 'whitesmoke', 'display': 'inline-block'}), 
                html.Div([
                                          html.Img(src='data:image/png;base64,{}'.format(encoded_image_RapaNui), 
                                   style={'height':'100%', 'width':'100%'})],
                                     style={'display': 'inline-block', 'float':'right', 'width': '50%'}), 
                html.H1("Perfiles Verticales", style={'text-align': 'center', 'color': '#0668a1','backgroundColor':'white'}),
      html.Div([ html.Label('Date Range:'),
            dcc.DatePickerRange(
                id='calendar_1',
                start_date=date(2015, 4, 10),
                end_date=date(2019,11,15)
                )], style={'backgroundColor':'white'}),
      html.Div([html.Label('Estructura Vertical de:'), dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'O3 [ppbv]', 'value': 'O3_ppbv'},
            {'label': 'Temperature[K]', 'value': 'Temp'},
            {'label': 'RH', 'value':'RH'},
            {'label': 'O3 [mba]', 'value': 'O3_mba'},
            {'label': 'O3 [Du]', 'value': 'column'},
            {'label': 'U [m/s]', 'value': 'U'},
            {'label': 'V [m/s]', 'value': 'V'},
            {'label': 'O3 [ppbv]', 'value': 'O3_ppbv'},
            {'label': 'Theta [K]', 'value': 'Theta'},
            {'label': 'Theta e [K]', 'value': 'Theta_e'},
            {'label': 'Mixing Ratio [g/kg]', 'value': 'Mixing_Ratio'}
        ],
        value='O3_ppbv')], style={'widht':'15%'}
    ),dcc.Graph(id='fig1'),
      html.H1("Linea de Tendencia", style={'text-align': 'center', 'color': '#0668a1','backgroundColor':'white'}),
      html.Div([html.Label('Altura [Km]:'), dcc.Input(id='input1', type="number",
    placeholder='Ingrese un valor..',
    value=0.7)  

]),
        html.Div([html.Label('Tendencia: '),
                  html.Button('Lamsal', id='btn-Lamsal', n_clicks=0),
                  html.Button('Carbone', id='btn-Carbone', n_clicks=0),
                  html.Button('Linear', id='btn-Linear', n_clicks=0)]),
        
        html.Div([dcc.Graph(id='Tendency_graph')]),              
        html.H1("Diagrama de Cajas y Bigotes", style={'text-align': 'center','color': '#0668a1','backgroundColor':'White'})
     ,html.Div([html.Label('Altura [Km]:'), dcc.Input(id='input2',
    placeholder='Ingrese un valor',
    type='number',
    value=5)  

])   
    ,html.Div([html.Label('Intervalo de tiempo:'),
            dcc.DatePickerRange(
                id='calendar_2',
                start_date=date(2015, 4, 10),
                end_date=date(2019,11,15)
                )], style={'backgroundColor':'white'}),
    dcc.Graph(id="boxplot1", style={'backgroundColor':'white'}), 
    html.H1("Histograma", style={'text-align': 'center','color': '#0668a1','backgroundColor':'White'}),
    html.Div([html.Label('Altura [Km]:'), dcc.Input(id='input3',
    placeholder='Enter a value...',
    type='number',
    value=0.7)  

]),
    html.Div([html.Label('Intervalo de Tiempo:'),
            dcc.DatePickerRange(
                id='calendar_3',
                start_date=date(2015, 4, 10),
                end_date=date(2019,11,15)
                )], style={'backgroundColor':'white'}),
    dcc.Graph(id="histogram", style={'backgroundColor':'white'}),
    html.Div([dcc.Markdown(dedent(f'''CITATION – If you use this dataset please acknowledge the Chilean Weather Office, and cite L. Gallardo, A. Henríquez, A. M. Thompson, R. Rondanelli, J. Carrasco, A. Orfanoz-Cheuquelaf and P. Velásquez, The first twenty years (1994-2014) of Ozone soundings from Rapa Nui (27°S, 109°W, 51m a.s.l.), Tellus B, 2016. (DOI: 10.3402/tellusb.v68.29484)

View in Tellus'''))]),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image_bot), 
              style={'height':'10%', 'width':'100%'})
], 'Espanish'
@app.callback(Output('fig1', 'figure'),
              Input('dropdown', 'value'),
              Input('calendar_1', 'start_date'),
              Input('calendar_1', 'end_date'),)

def update_graph(dropdown_name, start_date, end_date):
    a = ozonosondes_data.copy()
    a.index = a.index.strftime('%Y-%m-%d')
    g = a.loc[start_date:end_date]
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x = g[dropdown_name], 
                              y = g['Alt'],
                  name="DMC Measurement", mode='markers', 
                  marker={'opacity':0.5, 'size':6
                          ,
                  'line':{'width': 0.5, 'color': 'white'}})
                  )
    return fig1
@app.callback(Output('Tendency_graph', 'figure'),
              Input('btn-Lamsal', 'n_clicks'),
              Input('btn-Carbone', 'n_clicks'),
              Input('btn-Linear', 'n_clicks'),
              Input('Language', 'children'),
              Input('input1', 'value'))
def update_graph(btn1, btn2, btn3, Language, input1):
    
    df = ozonosondes_data[ozonosondes_data['Alt']==input1]
    #aux_a , aux_b = info_data('2015-01-01 01','2020-08-09 23',df,'D')

    df_m = df.resample('M').mean()["O3_ppbv"]
    df_m_aux  = df_m.fillna(df_m.mean())
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if (changed_id=='.')==True:
       
        def model(t, coeffs):
            return  (coeffs[0] + coeffs[1]*t + coeffs[2]*np.sin(2*np.pi*t/12) + coeffs[3]*np.cos(2*np.pi*t/12) +
                    coeffs[4]*np.sin(4*np.pi*t/12) + coeffs[5]*np.cos(4*np.pi*t/12) + 
                    coeffs[6]*np.sin(6*np.pi*t/12) + coeffs[7]*np.cos(6*np.pi*t/12) +
                    coeffs[8]*np.sin(8*np.pi*t/12) + coeffs[9]*np.cos(8*np.pi*t/12) +
                    coeffs[10]*np.sin(10*np.pi*t/12) + coeffs[11]*np.cos(10*np.pi*t/12) +
                    coeffs[12]*np.sin(12*np.pi*t/12) + coeffs[13]*np.cos(12*np.pi*t/12) +
                    coeffs[14]*np.sin(14*np.pi*t/12) + coeffs[15]*np.cos(14*np.pi*t/12) +
                    coeffs[15]*np.sin(16*np.pi*t/12) + coeffs[16]*np.cos(16*np.pi*t/12) +
                    coeffs[17]*np.sin(18*np.pi*t/12) + coeffs[18]*np.cos(18*np.pi*t/12) 
        )
    
        def residuals(coeffs, y, t):
            return y - model(t, coeffs)
        
        
        x0 = np.array([1, 1 ,1, 1,1 ,1,1,1,1,1,1,1,1,1,1,1,1,1,1], dtype=float)
    
        t = np.arange(len(df_m_aux))
        x, flag = leastsq(residuals, x0, args=(df_m_aux.values, t))
        model_trend =  model(t, x)
    elif 'btn-Lamsal' in changed_id:
       
        def model(t, coeffs):
            return  (coeffs[0] + coeffs[1]*t + coeffs[2]*np.sin(2*np.pi*t/12) + coeffs[3]*np.cos(2*np.pi*t/12) +
                    coeffs[4]*np.sin(4*np.pi*t/12) + coeffs[5]*np.cos(4*np.pi*t/12) + 
                    coeffs[6]*np.sin(6*np.pi*t/12) + coeffs[7]*np.cos(6*np.pi*t/12) +
                    coeffs[8]*np.sin(8*np.pi*t/12) + coeffs[9]*np.cos(8*np.pi*t/12) +
                    coeffs[10]*np.sin(10*np.pi*t/12) + coeffs[11]*np.cos(10*np.pi*t/12) +
                    coeffs[12]*np.sin(12*np.pi*t/12) + coeffs[13]*np.cos(12*np.pi*t/12) +
                    coeffs[14]*np.sin(14*np.pi*t/12) + coeffs[15]*np.cos(14*np.pi*t/12) +
                    coeffs[15]*np.sin(16*np.pi*t/12) + coeffs[16]*np.cos(16*np.pi*t/12) +
                    coeffs[17]*np.sin(18*np.pi*t/12) + coeffs[18]*np.cos(18*np.pi*t/12) 
        )
    
        def residuals(coeffs, y, t):
            return y - model(t, coeffs)
        
        
        x0 = np.array([1, 1 ,1, 1,1 ,1,1,1,1,1,1,1,1,1,1,1,1,1,1], dtype=float)
    
        t = np.arange(len(df_m_aux))
        x, flag = leastsq(residuals, x0, args=(df_m_aux.values, t))
        model_trend =  model(t, x)    


    elif 'btn-Linear' in changed_id:
 
        def model(t, coeffs):
            return  (coeffs[0] + coeffs[1]*t )
    
        def residuals(coeffs, y, t):
            return y - model(t, coeffs)
        
        
        x0 = np.array([1, 1], dtype=float)
    
        t = np.arange(len(df_m_aux))
        x, flag = leastsq(residuals, x0, args=(df_m_aux.values, t))
        model_trend =  model(t, x)    

    if Language== 'English':
        info = ["Decadal Tendency = " + str(round(x[1]*10*12,1)) + ' +/- xx [ppbv]  <br>Mean= '+ str(round(df["O3_ppbv"].mean(),1)) + " [ppbv]"]
        xlabel = 'Date'
    elif Language == 'Espanish': 
        info = ["Tendencia Decadal= " + str(round(x[1]*10*12,1)) + ' +/- xx [ppbv]  <br>Promedio= '+ str(round(df["O3_ppbv"].mean(),1)) + " [ppbv]"]
        xlabel= 'Fecha'
    fig = go.Figure()  
    fig.add_trace(go.Scatter(
            x=df.index,
            y=df["O3_ppbv"],
            mode='markers',
            #text = aux_a    ,  
            marker={
                'size': 9,
                #'color': aux_b,
                'opacity': 0.5,
                'line': {'width': 0.9, 'color': 'black'}
            }
        ))
    fig.add_trace(go.Scatter( 
                x=df_m.index, 
                y=model_trend,
                mode='markers', 
                marker=dict(size= 8, color='black')
                ))
    fig.add_trace(go.Scatter( 
                x=df_m.index[0:1], 
                y= [df["O3_ppbv"].max()*0.8 , df["O3_ppbv"].max()*0.8] , #df_m[0:1]*2.0
                mode='text', 
                marker=dict(size= 8, color='black'),
                text=info,
                textposition="top right",
                textfont=dict(
                family="Times New Roman",
                size=18,
                color="black")  #
                ))
    fig.update_layout(
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        title_font_color = 'dimgray',
        plot_bgcolor='white',
        paper_bgcolor='white',
        titlefont=dict(size=14,color='black'),
        xaxis_title=xlabel,
        yaxis_title="O<sub>3</sub> [ppbv]")
    return fig        
@app.callback(
    Output('boxplot1', 'figure'),
      [Input('calendar_2', 'start_date'),
      Input('calendar_2', 'end_date'),
      Input('Language','children'),
      Input('input2', 'value')
      ])
def update_graph(start_date, end_date, Language, input2):
    g = ozonosondes_data[ozonosondes_data['Alt']==input2]
    mat_h = g.set_index(g.index.month, append=False).unstack()['O3_ppbv']
    fig = px.box(mat_h, x=mat_h.index, y=mat_h.values, points=False)
    if Language == 'English':
        aux1 = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        xlabel = 'Month'
    elif Language == 'Espanish':
        aux1 = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        xlabel = 'Mes' 
    aux2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 , 12]

    
    fig.update_layout(
    #    autosize=False,
    #    width=500,
    #    height=500,
        #title = zaxis6_name,
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        title_font_color = 'dimgray',
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis=dict(
            #title_text= '<b>' + yaxis6_name + '</b>', 
        titlefont=dict(size=14,color='black')),
        xaxis=dict(
            #title_text="<b>"+ radio2_name + "</b> ",
            ticktext=aux1,
            tickvals=aux2,
    #        tickmode="array",
        titlefont=dict(size=14,color='black'),
      ),xaxis_title=xlabel,
        yaxis_title="O<sub>3</sub> [ppbv]")
    return fig        

@app.callback(
    Output('histogram', 'figure'),
      [Input('calendar_3', 'start_date'),
      Input('calendar_3', 'end_date'),
      Input('Language','children'),
      Input('input3', 'value')
      ])
def update_graph(start_date, end_date, Language, input3):
    a = ozonosondes_data.copy()
    a.index = a.index.strftime('%Y-%m-%d')
    g = a.loc[start_date:end_date]
    g = g[g['Alt']==input3]
    fig = px.histogram(g, x=g.O3_ppbv, histnorm='probability density')
    if Language == 'English':
        ylabel = 'Probability Density'
    if Language == 'Espanish':
        ylabel = 'Probabilidad'
    fig.update_layout(
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        title_font_color = 'dimgray',
        plot_bgcolor='white',
        paper_bgcolor='white',
        titlefont=dict(size=14,color='black'),
        yaxis_title=ylabel,
        xaxis_title="O<sub>3</sub> [ppbv]")    
    return fig              
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
    
    