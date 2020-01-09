
from flask import Flask, request
import os
import pandas as pd
import plotly.figure_factory as ff
from flask_cors import CORS
import math

basedir=os.path.abspath(os.path.dirname(__file__)) # root directory
server = Flask(__name__)
CORS(server, supports_credentials=True)

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
       {
    "data": [
        {
            "mode": "lines",
            "type": "scatter",
            "x": [
                24.049999999981424,
                25.0850855369356,
                null,
               ...
               ]
              }
    ],
    "layout": {
        "hovermode": "closest",
        "template": {
            "data": {
                "bar": [
                .....
                ....
                
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
    u = data.groupby('PinCharacteristic')['∆X'].mean()
    v = data.groupby('PinCharacteristic')['∆Y'].mean()
    U = 2 * (u / (u ** 2 + v ** 2).apply(lambda x: math.sqrt(x)))
    V = 2 * (v / (u ** 2 + v ** 2).apply(lambda x: math.sqrt(x)))
    fig = ff.create_quiver(data.groupby('PinCharacteristic')['x'].mean(), data.groupby('PinCharacteristic')['y'].mean(),U, V, scale=1, arrow_scale=0.2, angle=math.pi / 4, scaleratio=1)
    return fig.to_json()

if __name__ == '__main__':
    server.run(debug=True,port=8080)
