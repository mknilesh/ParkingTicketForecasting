# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
from dash import Dash, dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import json
import plotly.express as px
import pandas as pd
import dash_cytoscape as cyto
cyto.load_extra_layouts()
from datetime import date
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

app = Dash(__name__)

arima = pd.read_csv("arima.csv")
arima['Date'] = pd.to_datetime(arima['Issue Date'])

var = pd.read_csv("VAR.csv")
var['Date'] = pd.to_datetime(var['Date'])

gradient = pd.read_csv("gradient.csv")
gradient['Date'] = pd.to_datetime(gradient['Date'])


c = gradient.drop('Date',axis = 1)

cols = gradient.columns.tolist()[1:]

app = Dash(external_stylesheets=[dbc.themes.DARKLY])
load_figure_template('DARKLY')

app.layout = html.Div(children=[
    html.H1(children='Parking Data Vizualization', style={"alignContent":"center"}),

    html.Label('Please select the precinct for which you would like to visualize parking ticket forcasting along with the desired forecasting method'),
    html.Br(),

    dcc.Dropdown(cols,
                [],
                multi=False,
                id='asset-select',
                style={'color': 'black'}),

    html.Br(),

    dcc.Dropdown(['Gradient Boosted Regression', 'Arima Regression','VAR'],'Gradient Boosted Regression', 
                id='forecasting-dropdown', style={'color': 'black'}),

    html.Br(),
        
    dcc.Graph(id='line-chart'),


    
    html.Br(),

    html.Div([
        html.Br(),
        html.Label('Please select a date range for which to predict parking ticket', id='my-date-picker-range-al'),
        html.Br(),
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed= date(2017, 1, 1),
            max_date_allowed= date(2017, 12, 31),
            initial_visible_month=date(2016, 12, 21)
            ),
    ], id='my-date-picker-range-div', style={'display':'block'}),
    
    html.Br(),
        
    dcc.Graph(id='bar-chart'),
], style={'margin' : '20px'})


@app.callback(
    Output('line-chart', 'figure'),
    Input('asset-select', 'value'),
    Input('forecasting-dropdown', 'value'),
)
def update_figure(selected_precinct, forecast_method):

    if (len(selected_precinct) == 0):
        selected_precinct = "5"

    fig = go.Figure()

    df = None
    
    var_check = 0

    if forecast_method == "Gradient Boosted Regression":
        df = gradient
    elif forecast_method == "Arima Regression":
        df = arima
        var_check = 2
    else:
        df = var
        var_check = 1

    data = {}

    if var_check == 1:
        with open('sample2.json') as json_file:
            data = json.load(json_file)
    elif var_check == 2:
        with open('sample3.json') as json_file:
            data = json.load(json_file)
    else:
        with open('sample.json') as json_file:
            data = json.load(json_file)

    dict_date = data[selected_precinct][0]
    count = data[selected_precinct][1]
 
    fig.add_trace(go.Scatter(x=dict_date, y=count,mode='lines',name=f"Historical data for Precinct # {selected_precinct}"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df[selected_precinct],mode='lines',name=f"Forecasted data for Precinct # {selected_precinct}"))


    fig.update_layout(title='Parking Ticket Forecasting',
                        xaxis_title='Date',
                        yaxis_title='Number of Parking Tickets')
    return fig

@app.callback(
    Output('bar-chart', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
    )
def update_elements(start_date,end_date):

    if (start_date == None):
        start_date = "2017-01-01"
    
    if (end_date == None):
        end_date = "2017-04-01"

    date_data = gradient.loc[(gradient["Date"] >= start_date) & (gradient["Date"] < end_date)]
    date_sums = date_data.sum().T
    bar_data = pd.DataFrame(zip(gradient.columns[1:].values, date_sums), columns=["Precinct Number", "Predicted Parking Ticket Amount"])
    fig = px.bar(bar_data, x="Precinct Number", y="Predicted Parking Ticket Amount")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)