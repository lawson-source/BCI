# -*- coding: utf-8 -*-

import os
import sys
import itertools
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np


app = Flask(__name__)
CORS(app, supports_credentials=True)
basedir = os.path.abspath(os.path.dirname(__file__))

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
@app.route('/scatter', methods=['get', 'post'])
def scatter():
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')

    # read_csv
    data = pd.read_csv(basedir + '/data/09-2.csv')
    data['Production Date'] = pd.to_datetime(data['Production Date'].str.replace(' ASIA/SHANGHAI', ''),
                                             format='%d-%b-%y %I.%M.%S.%f %p', errors='ignore').astype('str')
    data = data[(start_date < data['Production Date']) & (data['Production Date'] < end_date)]
    data = data[['X', 'Y', 'Ident No.', 'PinCharacteristic']]

    # sql
    # sql = 'SELECT * FROM `data` WHERE `Production Date`>\'%s\' AND `Production Date`<\'%s\'' % (start_date, end_date)
    # engine = create_engine("mysql+pymysql://root:yuan20112@localhost/wujin?charset=UTF8MB4")
    # data = pd.read_sql(sql, engine)

    return data.to_json(orient='records')


""" 
param:
      start_date(date）: the start date of display data
      end_date(date): the end date of display data
      filter_condition(dict): the condition of filter, including the filter column name and column value
example:
      post:{"start_date":"2019-09-10","end_date":"2019-09-31","filter_condition":{"MouldMachineNo":"1","matDataBComponents[1].vendor":"370654167"}}
return:
[
  {"Ident No.":"36952126081905153330A20028","Deviation":0.937583},
  {"Ident No.":"36952126081905153330A20029","Deviation":0.496834},
 .
 .
 .
]
"""


@app.route('/frequency', methods=['get', 'post'])
def frequency():
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    filter_condition = request.json.get('filter_condition')
    data = pd.read_csv(basedir + '/data/total_data.csv')
    data = data[(start_date < data['Production Date']) & (data['Production Date'] < end_date)]
    # sql
    # data = ld.load_data(start_date=start_date, end_date=end_date).load_data()
    for column_name in list(filter_condition.keys()):
        if filter_condition[column_name]==None:
            continue
        else:
            data = data[data[column_name].astype('str') == str(filter_condition[column_name])]
    data = data[['Ident No.', 'Deviation']]

    return data.to_json(orient='records')


"""
param:
      start_time(datetime): the start time of counting defective percentage 
      end_time(datetime):the end time of counting defective percentage
method:
      the amount of product and defective product, deviation of which is above 0.5, is counted between start_time and end_time.
example:
      post:{"start_time":"2019-09-22 10:00:00","end_time":"2019-09-31 23:59:59"}

return:
       { "2019-09-31 23:59:59": 0.04478323010957599 }
"""


@app.route('/spc', methods=['get', 'post'])
def spc():
    end_time = request.json.get('end_time')
    start_time = request.json.get('start_time')
    data = pd.read_csv(basedir + '/data/total_data.csv')
    data = data[(start_time < data['Production Date']) & (data['Production Date'] < end_time)]
    # sql
    # data = ld.load_data(start_date=start_date, end_date=end_date).load_data()
    toatal = data.shape[0]
    defective_count = data[data['Deviation'] > 0.5].shape[0]
    defective= defective_count / (toatal + sys.float_info.epsilon)
    return jsonify({end_time: defective})





""" 
param:
      start_date(date）: the start date of display data
      end_date(date): the end date of display data
      filter_condition(dict): the condition of filter, including the filter column name and column value (allow None)
example:
     {"start_date":"2019-09-10","end_date":"2019-09-31","filter_condition":{"MouldMachineNo":"1","matDataBComponents[1].vendor":"370654167"}}
     or 
     {"start_date":"2019-09-10","end_date":"2019-09-31","filter_condition":{"MouldMachineNo":"","matDataBComponents[1].vendor":""}}

return:
{
    "{'MouldMachineNo': '1', 'matDataBComponents[1].vendor': '370654167'}": 0.029160982264665757
}
"""


@app.route('/RCA', methods=['get', 'post'])
def count_value_confidece():
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    filter_condition = request.json.get('filter_condition')

    # read_csv
    data = pd.read_csv(basedir + '/data/total_data.csv')
    data = data[(start_date < data['Production Date']) & (data['Production Date'] < end_date)]

    # sql
    # data = ld.load_data(start_date=start_date, end_date=end_date).load_data()
    items = []
    condition = []
    for column in list(filter_condition.keys()):
        if filter_condition[column] == "":
            items.append(column)
        else:
            data = data[data[column].astype('str') == filter_condition[column]]
            condition.append(column + '__' + filter_condition[column])
            items.append(column)
    for column in items:
        data[column] = column + '__' + data[column].astype('str')
    def count(item):
        result_item = data.groupby(item)['Deviation'].agg(['mean', 'count', 'sum'])
        return result_item

    result_list = count(items)
    result_item = pd.DataFrame(
        {'item': result_list.index.values, 'mean': result_list['mean'], 'sum': result_list['sum'],
         'count': result_list['count']})
    result_item = result_item[result_item['sum'] > 0.1 * result_item.shape[0]].sort_values('mean',
                                                                                           ascending=False).head(10)
    confidece = jsonify({'X': {'columns_values': result_item['item'].to_json(orient='values')},
                         'Y': {"confidece": result_item['mean'].to_json(orient='values')}})
    return confidece

""" 
param:
      start_date(date）: the start date of display data
      end_date(date): the end date of display data
example:
     {"start_date":"2019-09-10","end_date":"2019-09-31",}

return: csv file

"""
@app.route('/auto_suggestion',methods=['get', 'post'])
def auto_suggestion():
    columns=[  'matDataBComponents[1].batch',
                'matDataBComponents[1].vendor', 'matDataBComponents[2].batch',
                'matDataBComponents[2].vendor', 'matDataBComponents[3].batch',
                'matDataBComponents[3].vendor', 'matDataBComponents[4].batch',
                'matDataBComponents[4].vendor', 'toolData[1].toolID',
                'toolData[12].toolID', 'toolData[2].toolID',
               'MouldMachineNo',
                'MouldNestNo', 'TablePosition', 'Moulding.toolData[1].toolID',
                'Moulding.toolData[2].toolID', 'Moulding.toolData[3].toolID',
                'Moulding.toolData[4].toolID', 'Moulding.toolData[5].toolID',
                'Moulding.toolData[6].toolID', 'Moulding.toolData[7].toolID',]
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')

    # read_csv
    data = pd.read_csv(basedir + '/data/total_data.csv')
    data = data[(start_date < data['Production Date']) & (data['Production Date'] < end_date)]

    # sql
    # data = ld.load_data(start_date=start_date, end_date=end_date).load_data()

    data.loc[data.Deviation < 0.5, 'Deviation'] = 0
    data.loc[data.Deviation >= 0.5, 'Deviation'] = 1
    for column in columns:
        data[column] = column + '__' + data[column]
    data2 = data.drop_duplicates(columns)

    def count(item):
        result_item_1 = data.groupby(item)['Deviation'].agg(['mean', 'count', 'sum'])
        result_item_2=data2.groupby(item)['Deviation'].agg(['count', ]).rename(columns={'count': 'ccount'})
        result_item = pd.merge(result_item_1,result_item_2,left_index=True, right_index=True)
        return result_item

    result = pd.DataFrame(columns=['mean', 'sum', 'count', 'ccount'])
    for i in range(1, 7):
        result_list = list(map(count, list(itertools.combinations(columns, i))))
        result_list = pd.concat(result_list)
        result_list = result_list[(result_list['ccount'] / result_list['count'] > 0.5) & (result_list['count'] > 100)]
        result = result.append(result_list).sort_values('mean', ascending=False).head(20)
    result.head(10).to_csv(basedir+'suggestion.csv')
    return jsonify('success')


if __name__ == '__main__':
    app.run(debug=True, port='8880')
