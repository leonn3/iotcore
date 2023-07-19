# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 12:19:31 2023

@author: a816959
"""

import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import dash_daq as daq

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from flask import Flask, jsonify, request
from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url
from dash import Input, Output, html, State, Dash, dash_table, callback
import plotly.express as px
from datetime import datetime, timedelta
from datetime import date
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import pyodbc
from plotly.subplots import make_subplots

# Configuração da conexão SQL Server
sql_server = "192.168.1.23"
sql_database = "IOT"
sql_username = "sa"
sql_password = "Wlp23@280@03"

server_flask = Flask(__name__)
#app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR],server=server_flask)
app = Dash(__name__, external_stylesheets=[dbc.themes.YETI],server=server_flask)

# select the Bootstrap stylesheet2 and figure template2 for the theme toggle here:
template_theme1 = "yeti"
template_theme2 = "darkly"
url_theme1 = dbc.themes.YETI
url_theme2 = dbc.themes.DARKLY

color_bar_menu="dark" #"MidnightBlue", #id: navbar-theme
slidebar_background_color = "dark"#"GhostWhite", #id="sidebar"
template_indicator="seaborn" #"plotly_dark" #"seaborn" #"simple_white" #"seaborn" 
dark_ = True, #id: navbar-theme

##### body ####################################################################
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": slidebar_background_color,
    #"background-color":"#7f7f7f",
    #"background-color": "#f8f9fa",
}


CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "0rem 0rem",
    "white-space": "nowrap",
}

CONTENT_STYLE2 = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "0rem 0rem",
    "position": "center",
    "align-items": "center",
    "justify-content": "center",
    "align":"center"
}

BUTTON_STYLE = {
  "width": "352px",
  "height": "76px",
  "line-height": "78px",
  "font-size": "20px",
  "font-family": "VALORANT", #"Bebas Neue", 
  "background": "linear-gradient(45deg, transparent 5%, #FF013C 5%)",
  "border": "0",
  "color": "#fff",
  "letter-spacing": "3px",
  "box-shadow": "6px 0px 0px #00E6F6",
  "outline": "transparent",
  "position": "relative",
  "user-select": "none",
  "-webkit-user-select": "none",
  "touch-action": "manipulation",
  'textAlign' : 'center',
  "align-items": "center",
  "justify-content": "center",
}

TITLE_STYLE = {
  "width": "1000px",
  "height": "66px",
  "line-height": "78px",
  "font-size": "20px",
  "font-family": "VALORANT", #"Bebas Neue", 
  "background": "linear-gradient(45deg, transparent 5%, #FF013C 5%)",
  "border": "0",
  "color": "#fff",
  "letter-spacing": "3px",
  "box-shadow": "6px 0px 0px #00E6F6",
  "outline": "transparent",
  "position": "relative",
  "user-select": "none",
  "-webkit-user-select": "none",
  "touch-action": "manipulation",
  'textAlign' : 'center',
  "align-items": "center",
  "justify-content": "center",
  "display": "flex",
}

BODY_STYLE = {
  "align-items": "center",
  #"background-image": "linear-gradient(144deg,#AF40FF, #5B42F3 50%,#00DDEB)",
  "border": "2px",
  "border-radius": "8px",
  "box-shadow": "rgba(151, 65, 252, 0.2) 0 15px 30px -5px",
  "box-sizing": "border-box",
  "color": "#FFFFFF",
  "display": "flex",
  "font-family": "Phantomsans",
  "font-size": "20px",
  "justify-content": "center",
  "line-height": "1em",
  "max-width": "100%",
  "min-width": "140px",
  "padding": "3px",
  "text-decoration": "none",
  "user-select": "none",
  "-webkit-user-select": "none",
  "touch-action": "manipulation",
  "white-space": "nowrap",
  "cursor": "pointer",
}

MENU_STYLE = {
    "margin-left": "0rem",
    "margin-right": "0rem",
    "padding": "1rem 0rem",
}

VALORANT_STYLE = {
    "font-family": "VALORANT",
    "font-size": "30px",
}

VALORANT_STYLE_CARD_TITLE  = {
    #"font-family": "Bebas Neue", #"VALORANT",
    "font-size": "12px",
    'textAlign' : 'center',
    'align-items': 'center', 
}

STYLE_CARDS = {'width': '100%', 
               'align-items': 'top', 
               'textAlign' : 'center',
               #"font-family": "Bebas Neue", #"VALORANT",
               'font-size':'2',
               }

PLOTLY_LOGO = "https://ppa.org.br/wp-content/uploads/2020/09/Logo-oficial-ALBRAS-png-300x207.png"

nav_item = dbc.NavItem(
        dbc.NavLink("Suporte", href="mailto:woldson.gomes@albras.net?CC=wleonne@hotmail.com&Subject=Ajuda%3A%20Painel%20IOT%20Core&Body=Favor%20descreva%20sua%20solicita%E7%E3o%20aqui%3A%0A%0A-%3E%20"))
                       
nav_item2 = dbc.NavItem(
        dbc.NavLink("Grafana", href="https://hydroalbras.stratws.com/"))

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("About", id="dropdown-button1", n_clicks=0),
        dbc.DropdownMenuItem("Help", id="dropdown-button2", n_clicks=0),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Logout", id="dropdown-button3", n_clicks=0),
        dbc.DropdownMenuItem(divider=True),
        #ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2],),
        dbc.DropdownMenuItem(dbc.Col([(ThemeChangerAIO(aio_id="theme", radio_props={"value":dbc.themes.YETI}))], align="end")),
        #dbc.DropdownMenuItem(ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]))
    ],
    nav=True,
    in_navbar=True,
    label="Menu",
)

dropdown2 = dbc.DropdownMenu([
        dbc.DropdownMenuItem("Cyborg", id="Cyborg", n_clicks=0),
        dbc.DropdownMenuItem("Vapor", id="Vapor", n_clicks=0),
        dbc.DropdownMenuItem("Journal", id="Journal", n_clicks=0),
        dbc.DropdownMenuItem("Lumen", id="Lumen", n_clicks=0),
        dbc.DropdownMenuItem("Lux", id="Lux", n_clicks=0),
        dbc.DropdownMenuItem("Minty", id="Minty", n_clicks=0),
        dbc.DropdownMenuItem("Morph", id="Morph", n_clicks=0),
        dbc.DropdownMenuItem("Quartz", id="Quartz", n_clicks=0),
        dbc.DropdownMenuItem("Sketchy", id="Sketchy", n_clicks=0),
        dbc.DropdownMenuItem("Slate", id="Slate", n_clicks=0),
        dbc.DropdownMenuItem("Solar", id="Solar", n_clicks=0),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Darkly", id="Darkly", n_clicks=0),
        dbc.DropdownMenuItem("Bootstrap", id="Bootstrap", n_clicks=0),
    ],
    nav=True,
    in_navbar=True,
    label="Theme",
    id="Theme",
)

datepicker = html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',
        # display_format='MMMM DD, Y',
        display_format='MMMM DD',
        clearable=True,
        with_portal=True,
        min_date_allowed=date(2021, 1, 1),
        max_date_allowed=date.today() + timedelta(days=5),
        initial_visible_month=date.today() - timedelta(days=30),
        start_date = date.today() - timedelta(days=30),
        end_date = date.today() + timedelta(days=1),
    ),
    html.Div(id='output-container-date-picker-range')
],style=CONTENT_STYLE)

logo = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                     [  dbc.Col(html.Img(src=PLOTLY_LOGO, height="60px")),
                        #dbc.Col(html.Img(src=PLOTLY_LOGO_AM, height="60px")),
                        #dbc.Col(dbc.NavbarBrand("Machine Learning for Fluoridation Predict", className="ms-2")),
                        dbc.Col(dbc.NavbarBrand("IOT CORE", className="ms-3",style=VALORANT_STYLE)),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://www.hydro.com/pt-BR/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler1", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [dbc.Col([ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2])],align="center"), datepicker, nav_item, nav_item2, dropdown],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse1",
                navbar=True,
            ),
        ],
    ),
    id = "navbar-theme",
    color=color_bar_menu,
    dark=dark_,
    className="mb-5",
    style=MENU_STYLE,
)


submit =  dbc.Col(dbc.Button("SUBMIT", id="submit", className="me-2", size="lg", n_clicks=0,style=BUTTON_STYLE))
        

app.layout = html.Div([
    #dcc.Store(id='memory-output'),
    #dcc.Location(id="url"),
    logo,
    html.Div(id="sidebar"),
    
    ####### LINHA DE CARDS ##########
    dbc.Row([
        
    ########## LED INDICATOR ################
    dbc.Col(
    html.Div([
        dbc.Row([
        html.H5(id="status-text",
        style=VALORANT_STYLE_CARD_TITLE,
            ),]),
        dbc.Row([
        daq.Indicator(
        id='my-indicator-1',
        label="-----------------",
    ),]),
        ],style=VALORANT_STYLE_CARD_TITLE,),
        ),
    ########################################CARD 1
    dbc.Col(
    html.Div([
    dbc.CardHeader([
        html.H5("Last Update",
        style=VALORANT_STYLE_CARD_TITLE,
            ),
        ]),
    dbc.CardBody(
        [
            html.H5(id='card1', className="card-title",
            style=STYLE_CARDS,
                ),
    ])]),
    ),
    
    ########################################CARD 2
    dbc.Col(
    html.Div([
    dbc.CardHeader([
        html.H5("Temp Average",
        style=VALORANT_STYLE_CARD_TITLE,
            ),
        ]),
    dbc.CardBody(
        [
            html.H5(id='card2', className="card-title",
            style=STYLE_CARDS,
                ),
    ])]),
    ),
    
    ########################################CARD 3
    dbc.Col(
    html.Div([
    dbc.CardHeader([
        html.H5("Imbalance KF Average",
        style=VALORANT_STYLE_CARD_TITLE,
            ),
        ]),
    dbc.CardBody(
        [
            html.H5(id='card3', className="card-title",
            style=STYLE_CARDS,
                ),
    ])]),
    ),

    ########################################CARD 4
    dbc.Col(
    html.Div([
    dbc.CardHeader([
        html.H5("Horimetro",
        style=VALORANT_STYLE_CARD_TITLE,
            ),
        ]),
    dbc.CardBody(
        [
            html.H5(id='card4', className="card-title",
            style=STYLE_CARDS,
                ),
    ])]),
    ),
    
    ],style=CONTENT_STYLE), 
    
    
    html.Br(), # Adiciona uma quebra de linha
    html.Br(), # Adiciona uma quebra de linha
    
    dbc.Row(
    [    
        html.Div([
        dbc.CardHeader("Time Analysis"),
        ],style=TITLE_STYLE),
    ],style=CONTENT_STYLE2),    
    
    html.Br(), # Adiciona uma quebra de linha
    html.Br(), # Adiciona uma quebra de linha
    
    html.Div([
    dbc.Row(
    [
     
        dbc.Col(
            
            dcc.Loading(
                        id="loading-1",
                        children=[html.Div([ 
                            html.Div(dcc.Graph(id="graph")),
                            ])],
                        type="graph", # 'graph', 'cube', 'circle', 'dot' or 'default'
                    ), md=4
            ),
        
        dbc.Col(
            
            dcc.Loading(
                        id="loading-2",
                        children=[html.Div([ 
                            html.Div(dcc.Graph(id="graph2")),
                            ])],
                        type="graph", # 'graph', 'cube', 'circle', 'dot' or 'default'
                    ), md=4
            ),
        
        dbc.Col(
            
            dcc.Loading(
                        id="loading-3",
                        children=[html.Div([ 
                            html.Div(dcc.Graph(id="graph3")),
                            ])],
                        type="graph", # 'graph', 'cube', 'circle', 'dot' or 'default'
                    ), md=4
            ),
    ]
    ),
    
    dbc.Row(
    [
        dbc.Col(
            
            dcc.Loading(
                        id="loading-4",
                        children=[html.Div([ 
                            html.Div(dcc.Graph(id="graph4")),
                            ])],
                        type="graph", # 'graph', 'cube', 'circle', 'dot' or 'default'
                    ), md=4
            ),
        
        
        dbc.Col(
            
            dcc.Loading(
                        id="loading-5",
                        children=[html.Div([ 
                            html.Div(dcc.Graph(id="graph5")),
                            ])],
                        type="graph", # 'graph', 'cube', 'circle', 'dot' or 'default'
                    ), md=4
            ),
        
        dbc.Col(
            
            dcc.Loading(
                        id="loading-6",
                        children=[html.Div([ 
                            html.Div(dcc.Graph(id="graph6")),
                            ])],
                        type="graph", # 'graph', 'cube', 'circle', 'dot' or 'default'
                    ), md=4
            ),
        
    ]
    ),
    
    html.Br(), # Adiciona uma quebra de linha
    html.Br(), # Adiciona uma quebra de linha
    
    dbc.Row(
    [    
        html.Div([
        dbc.CardHeader("Frequency Analysis"),
        ],style=TITLE_STYLE),
    ],style=CONTENT_STYLE2),        
    
    dcc.Loading(
                id="loading-11",
                children=[html.Div([ 
                    html.Div(dcc.Graph(id="graph11")),
                    ])],
                type="dot", # 'graph', 'cube', 'circle', 'dot' or 'default'
    ),
    
    
    #submit
    html.Br(), # Adiciona uma quebra de linha
    html.Br(), # Adiciona uma quebra de linha
    
    ],style=CONTENT_STYLE),
    ])


# we use a callback to toggle the collapse on small screens
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# the same function (toggle_navbar_collapse) is used in all three callbacks
for i in [1]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

@app.callback(
     Output("sidebar", "children"), 
     Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def update_graph_theme(toggle):
    template = template_theme2 if toggle else template_theme1
    return None


@app.callback(
    Output("graph", "figure"), 
    Output("graph2", "figure"),
    Output("graph3", "figure"),
    Output("graph4", "figure"),
    Output("graph5", "figure"),
    Output("graph6", "figure"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    start_date_object = date.fromisoformat(str(start_date))
    start_date_string = start_date_object.strftime('%Y-%m-%d %H:%M:%S')
    end_date_object = date.fromisoformat(str(end_date))
    end_date_string = end_date_object.strftime('%Y-%m-%d %H:%M:%S')
    
    #Connect to database
    conn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server="+sql_server+";"
        "Database="+sql_database+";"
        "UID="+sql_username+";"
        "PWD="+sql_password+";"
    )
    cursor = conn.cursor()
    query=f"SELECT [topic_],[value_],[time_] FROM [IOT].[dbo].[IOT] WHERE (topic_ = 'esp32/accelerationX' OR topic_ = 'esp32/accelerationY' OR topic_ = 'esp32/accelerationZ') AND (time_ BETWEEN '{start_date_string}' AND '{end_date_string}') ORDER BY time_ DESC"
    print(query)
    df = pd.read_sql(query, conn)

    fig = px.line(df, x='time_', y='value_', color='topic_', markers=True)
    
    fig.update_layout(
        yaxis_title="Acceleration [ m/s² ]",
        grid= dict(columns=1, rows=1),
        margin = dict(t=0, l=0, r=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    #Fig2 update
    query2=f"SELECT [topic_],[value_],[time_] FROM [IOT].[dbo].[IOT] WHERE (topic_ = 'esp32/rotationX' OR topic_ = 'esp32/rotationY' OR topic_ = 'esp32/rotationZ') AND (time_ BETWEEN '{start_date_string}' AND '{end_date_string}') ORDER BY time_ DESC"
    df2 = pd.read_sql(query2, conn)
    fig2 = px.line(df2, x='time_', y='value_', color='topic_', markers=True)
    fig2.update_layout(
        yaxis_title="Rotation [ rad/s ]",
        grid= dict(columns=1, rows=1),
        margin = dict(t=0, l=0, r=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    #Fig3 update
    query3=f"SELECT [topic_],[value_],[time_] FROM [IOT].[dbo].[IOT] WHERE (topic_ = 'esp32/current_R' OR topic_ = 'esp32/current_S' OR topic_ = 'esp32/current_T') AND (time_ BETWEEN '{start_date_string}' AND '{end_date_string}') ORDER BY time_ DESC"
    df3 = pd.read_sql(query3, conn)
    fig3 = px.line(df3, x='time_', y='value_', color='topic_', markers=True)
    fig3.update_layout(
        yaxis_title="Current [ A ]",
        grid= dict(columns=1, rows=1),
        margin = dict(t=0, l=0, r=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    #Fig4 update
    query4=f"SELECT [topic_],[value_],[time_] FROM [IOT].[dbo].[IOT] WHERE topic_ = 'esp32/temperature' AND time_ BETWEEN '{start_date_string}' AND '{end_date_string}' ORDER BY time_ DESC"
    df4 = pd.read_sql(query4, conn)
    fig4 = px.line(df4, x='time_', y='value_', color='topic_', markers=True)
    fig4.update_layout(
        yaxis_title="Temperature [ °C ]",
        grid= dict(columns=1, rows=1),
        margin = dict(t=0, l=0, r=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    #Fig5 update
    query=f"SELECT [topic_],[value_],[time_] FROM [IOT].[dbo].[IOT] WHERE (topic_ = 'esp32/imbalance' OR topic_ = 'esp32/imbalance_est_kf') AND time_ BETWEEN '{start_date_string}' AND '{end_date_string}' ORDER BY time_ DESC"
    df5 = pd.read_sql(query, conn)
    fig5 = px.line(df5, x='time_', y='value_', color='topic_', markers=True)
    fig5.update_layout(
        yaxis_title="Imbalance",
        grid= dict(columns=1, rows=1),
        margin = dict(t=0, l=0, r=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    #Fig6 update
    query=f"SELECT [topic_],[value_],[time_] FROM [IOT].[dbo].[IOT] WHERE (topic_ = 'esp32/status') AND time_ BETWEEN '{start_date_string}' AND '{end_date_string}' ORDER BY time_ DESC"
    df6 = pd.read_sql(query, conn)
    fig6 = px.area(df6, x='time_', y='value_', color='topic_', markers=True)
    fig6.update_layout(
        yaxis_title="Horimetro",
        grid= dict(columns=1, rows=1),
        margin = dict(t=0, l=0, r=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    
    cursor.close()
    conn.close()
    return fig, fig2, fig3, fig4, fig5, fig6

#####################################
@app.callback(
    Output("graph11", "figure"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output2(start_date, end_date):
    start_date_object = date.fromisoformat(str(start_date))
    start_date_string = start_date_object.strftime('%Y-%m-%d %H:%M:%S')
    end_date_object = date.fromisoformat(str(end_date))
    end_date_string = end_date_object.strftime('%Y-%m-%d %H:%M:%S')
    
    fig11 = make_subplots(rows=2, cols=3)
    
    #Connect to database
    conn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server="+sql_server+";"
        "Database="+sql_database+";"
        "UID="+sql_username+";"
        "PWD="+sql_password+";"
    )
    cursor = conn.cursor()
    query=f"SELECT [topic_],[value_],[time_] FROM [IOT].[dbo].[IOT] WHERE (topic_ = 'esp32/accelerationX' OR topic_ = 'esp32/accelerationY' OR topic_ = 'esp32/accelerationZ') AND (time_ BETWEEN '{start_date_string}' AND '{end_date_string}') ORDER BY time_ DESC"
    df = pd.read_sql(query, conn)
    query2=f"SELECT [topic_],[value_],[time_] FROM [IOT].[dbo].[IOT] WHERE (topic_ = 'esp32/rotationX' OR topic_ = 'esp32/rotationY' OR topic_ = 'esp32/rotationZ') AND (time_ BETWEEN '{start_date_string}' AND '{end_date_string}') ORDER BY time_ DESC"
    df2 = pd.read_sql(query2, conn)
    
    #FFT accelerationX
    data_ax_t = df[df.topic_.isin(['esp32/accelerationX'])].value_  
    n = len(data_ax_t) # tamanho da amostra
    timestep = 0.1 # tempo de amostragem
    freq = np.fft.fftfreq(n, d=timestep) # frequências
    fft_vals = np.abs(np.fft.fft(data_ax_t)) # valores da FFT
    array_fft = np.transpose(np.array([freq,fft_vals]))
    df_fft = pd.DataFrame(array_fft, columns=['freq','fft_vals'])
    
    #FFT accelerationY
    data_ay_t = df[df.topic_.isin(['esp32/accelerationY'])].value_  
    n = len(data_ay_t) # tamanho da amostra
    freq = np.fft.fftfreq(n, d=timestep) # frequências
    fft_vals = np.abs(np.fft.fft(data_ay_t)) # valores da FFT
    array_fft = np.transpose(np.array([freq,fft_vals]))
    df_fft_ay = pd.DataFrame(array_fft, columns=['freq','fft_vals'])

    #FFT accelerationZ
    data_az_t = df[df.topic_.isin(['esp32/accelerationZ'])].value_  
    n = len(data_az_t) # tamanho da amostra
    freq = np.fft.fftfreq(n, d=timestep) # frequências
    fft_vals = np.abs(np.fft.fft(data_az_t)) # valores da FFT
    array_fft = np.transpose(np.array([freq,fft_vals]))
    df_fft_az = pd.DataFrame(array_fft, columns=['freq','fft_vals'])
    
    #FFT rotationX
    data_rx_t = df2[df2.topic_.isin(['esp32/rotationX'])].value_  
    n = len(data_rx_t) # tamanho da amostra
    freq = np.fft.fftfreq(n, d=timestep) # frequências
    fft_vals = np.abs(np.fft.fft(data_rx_t)) # valores da FFT
    array_fft = np.transpose(np.array([freq,fft_vals]))
    df_fft_rx = pd.DataFrame(array_fft, columns=['freq','fft_vals'])

    #FFT rotationY
    data_ry_t = df2[df2.topic_.isin(['esp32/rotationY'])].value_  
    n = len(data_ry_t) # tamanho da amostra
    freq = np.fft.fftfreq(n, d=timestep) # frequências
    fft_vals = np.abs(np.fft.fft(data_ry_t)) # valores da FFT
    array_fft = np.transpose(np.array([freq,fft_vals]))
    df_fft_ry = pd.DataFrame(array_fft, columns=['freq','fft_vals'])

    
    #FFT rotationZ
    data_rz_t = df2[df2.topic_.isin(['esp32/rotationZ'])].value_  
    n = len(data_rz_t) # tamanho da amostra
    freq = np.fft.fftfreq(n, d=timestep) # frequências
    fft_vals = np.abs(np.fft.fft(data_rz_t)) # valores da FFT
    array_fft = np.transpose(np.array([freq,fft_vals]))
    df_fft_rz = pd.DataFrame(array_fft, columns=['freq','fft_vals'])
    
    
    fig11.add_trace(row=1, col=1,
        trace=go.Scatter(x=df_fft['freq'], y=df_fft['fft_vals'],
                            mode='markers+lines',
                            name='FFT [ Acceleration X ]'))
    
    fig11.add_trace(row=1, col=2,
        trace=go.Scatter(x=df_fft_ay['freq'], y=df_fft_ay['fft_vals'],
                            mode='markers+lines',
                            name='FFT [ Acceleration Y ]'))
    
    fig11.add_trace(row=1, col=3,
        trace=go.Scatter(x=df_fft_az['freq'], y=df_fft_az['fft_vals'],
                            mode='markers+lines',
                            name='FFT [ Acceleration Z ]'))
    
    
    
    fig11.add_trace(row=2, col=1,
        trace=go.Scatter(x=df_fft_rx['freq'], y=df_fft_rx['fft_vals'],
                            mode='markers+lines',
                            name='FFT [ Roll ]'))
    
    fig11.add_trace(row=2, col=2,
        trace=go.Scatter(x=df_fft_ry['freq'], y=df_fft_ry['fft_vals'],
                            mode='markers+lines',
                            name='FFT [ Pitch ]'))
    
    fig11.add_trace(row=2, col=3,
        trace=go.Scatter(x=df_fft_rz['freq'], y=df_fft_rz['fft_vals'],
                            mode='markers+lines',
                            name='FFT [ Yaw ]'))
    
    fig11.update_layout(
        #margin = dict(t=0, l=0, r=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    cursor.close()
    conn.close()
    return fig11
#####################################
@app.callback(
    Output('my-indicator-1', 'value'),
    Output(component_id='status-text', component_property='children'),
    Output(component_id='card1', component_property='children'),
    Output(component_id='card2', component_property='children'),
    Output(component_id='card3', component_property='children'),
    Output(component_id='card4', component_property='children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output_div(start_date, end_date):
    
    start_date_object = date.fromisoformat(str(start_date))
    start_date_string = start_date_object.strftime('%Y-%m-%d %H:%M:%S')
    end_date_object = date.fromisoformat(str(end_date))
    end_date_string = end_date_object.strftime('%Y-%m-%d %H:%M:%S')
    datetimenow = datetime.now()
    
    #Connect to database
    conn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server="+sql_server+";"
        "Database="+sql_database+";"
        "UID="+sql_username+";"
        "PWD="+sql_password+";"
    )
    cursor = conn.cursor()
    query=f"SELECT [topic_],[value_],[time_] FROM [IOT].[dbo].[IOT] WHERE (topic_ = 'esp32/temperature') AND (time_ BETWEEN '{start_date_string}' AND '{end_date_string}') ORDER BY time_ DESC"
    df_temp = pd.read_sql(query, conn)
    query=f"SELECT [topic_],[value_],[time_] FROM [IOT].[dbo].[IOT] WHERE (topic_ = 'esp32/imbalance_est_kf') AND (time_ BETWEEN '{start_date_string}' AND '{end_date_string}') ORDER BY time_ DESC"
    df_ikf = pd.read_sql(query, conn)
    query=f"SELECT [topic_],[value_],[time_] FROM [IOT].[dbo].[HORIMETRO]"
    df_horimetro = pd.read_sql(query, conn)
    
    mean_temp = str(round(np.mean(df_temp.value_),2))
    mean_ifk = str(round(np.mean(df_ikf.value_),2))
    
    #SELECT * FROM minha_tabela ORDER BY id DESC LIMIT 1;
    query=f"SELECT TOP(1) [topic_],[value_],[time_] FROM [IOT].[dbo].[IOT] WHERE (topic_ = 'esp32/status') ORDER BY time_ DESC"
    df_status = pd.read_sql(query, conn)
    
    if int(df_status['value_']) == 1:
        status_led = True
        status_text = 'Power ON'
    else:
        status_led = False
        status_text = 'Power OFF'
    
    cursor.close()
    conn.close()
    
    last_update = str(datetimenow.strftime('%Y-%m-%d %H:%M:%S'))
    return status_led, status_text, last_update, mean_temp, mean_ifk, df_horimetro.value_
#####################################



if __name__ == '__main__':
    app.run_server(host="0.0.0.0",port="8051")