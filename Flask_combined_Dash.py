import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask, request,  jsonify
import os, requests
import pandas as pd
from datetime import datetime as dt
import plotly.figure_factory as ff

basedir=os.path.abspath(os.path.dirname(__file__)) # root directory
server = Flask(__name__)

""" 
param:
      start_date(date）: the start date of display data
      end_date(date): the end date of display data
example:
      post:{"start_date":"2019-09-10","end_date":"2019-09-31"}
return:[
    {
        "X": 24.11165839,
        "Y": 42.84333982,
        "Ident No.": "36951100011909153330A20029",
        "PinCharacteristic": "D-PIN1 A"
    },
    {
        "X": 24.09777306,
        "Y": 37.8589999,
        "Ident No.": "36951100011909153330A20029",
        "PinCharacteristic": "D-PIN1 B"
    },
    .
    .
    .
    ]
"""
@server.route('/scatter', methods=['get', 'post'])
def scatter():
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    #read data sql from sql
    """ sql = 'SELECT * FROM `data` WHERE `Production Date`>\'%s\' AND `Production Date`<\'%s\'' % (start_date, end_date)
       engine = create_engine("mysql+pymysql://root:yuan20112@localhost/wujin?charset=UTF8MB4")
       data = pd.read_sql(sql, engine)"""


    # read data from_csv
    data = pd.read_csv(basedir + '/data/09-2.csv')
    data['Production Date'] = pd.to_datetime(data['Production Date'].str.replace(' ASIA/SHANGHAI', ''),
                                             format='%d-%b-%y %I.%M.%S.%f %p', errors='ignore').astype('str')
    data = data[(start_date < data['Production Date']) & (data['Production Date'] < end_date)]
    data=data[['X', 'Y', '∆X', '∆Y', 'Ident No.', 'PinCharacteristic']]
    data['x'] = data['X'] - data['∆X']
    data['y'] = data['Y'] - data['∆Y']



    return data.to_json(orient='records')

dash_app = dash.Dash(__name__,server=server,url_base_pathname='/pin/')

dash_app.layout=html.Div(id='container',children=[html.Div(id='date',
                                                          children= dcc.DatePickerRange(id='date-picker-range',
                                                                                        start_date_placeholder_text='Select a start date!',
                                                                                        start_date=dt(2019,9,10).date(),
                                                                                        end_date_placeholder_text='Select a end date!',
                                                                                        end_date=dt(2019,9,30).date(),
                                                                                        )
                                                          ),
                                                  html.Div(id='Graph',children=dcc.Graph(id='graph')
                                                           )
                                                  ]
                         )


@dash_app.callback(
Output('graph','figure'),
    [
        Input('date-picker-range','start_date'),
        Input('date-picker-range','end_date')
    ]
)
def update_graph(start_date,end_date):
    parm={"start_date":start_date,"end_date":end_date}
    reponse=requests.post(url='http://localhost:8888/scatter',json=parm)
    data = pd.DataFrame.from_dict(reponse.json())
    fig = ff.create_quiver(data.groupby('PinCharacteristic')['x'].mean(), data.groupby('PinCharacteristic')['y'].mean(), 100*data.groupby('PinCharacteristic')['∆X'].mean(), 100*data.groupby('PinCharacteristic')['∆Y'].mean())
    return  fig

if __name__ == '__main__':
    server.run(debug=True,port=8888)