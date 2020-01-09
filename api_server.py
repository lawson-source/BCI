import flask, json
from flask import render_template,  request
import pandas_profiling as pp
import pandas as pd

'''
POC: test inserting dash into flask
'''
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plot import generatePlot
import os
server = flask.Flask(__name__)
dirf=os.path.abspath(os.path.dirname(__file__)) # root directory
loc = dirf+'/Data matrix _20190802 V04.xlsx'
figure_plot = generatePlot(loc)

pin_plot = figure_plot[0]
correlation_plot = figure_plot[1]
correlation_plot_clustering = figure_plot[2]
toolData = figure_plot[4]

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
dash_app = dash.Dash(__name__,server=server, external_stylesheets=external_stylesheets,url_base_pathname='/dashboard/')

toolDiv = html.Div(
    [ html.H2("Individual Tool Accuracy Assessment",
                            style={'text-align':'center'})
       ,
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.H3("Tool Categories", style={
                                'margin-bottom': '10px'}),
                        dcc.RadioItems(
                            id='countries-dropdown',
                            options=[{'label': k, 'value': k}
                                     for k in toolData.keys()],
                            value=list(toolData.keys())[0],
                            labelStyle={'display': 'block',
                                        'text-align': 'justify'}

                        ),
                        html.H3("Tool IDs", style={'margin-bottom': '10px'}),
                        dcc.RadioItems(
                            id='cities-dropdown',
                            labelStyle={'display': 'block',
                                        'text-align': 'justify'
                                        }
                        )
                    ]),

                width=2
                ),

                dbc.Col(
                    html.Div([
                        html.Div([
                            html.Span(id='tool_cat', style={
                                      'margin-bottom': '3px', 'display': 'inline-block', 'color': '#8a8a8a', 'font-size': '15px'}),
                            html.Span(children=' : ', style={'margin-bottom': '3px', 'margin-right': '5px',
                                                             'margin-left': '5px', 'display': 'inline-block', 'color': '#8a8a8a', 'font-size': '15px'}),
                            html.Span(id='tool_id', style={
                                      'margin-bottom': '0px', 'display': 'inline-block', 'color': '#8a8a8a', 'font-size': '15px'})
                        ]),
                        html.Hr(),
                        html.H3("Deviation", style={
                                'margin-bottom': '10px', 'margin-top': '20px'}),
                        html.Div(id='tool_deviation', style={
                                 'font-size': '20px', 'color': '#0c6093'}),
                        html.Hr(),
                        html.H3("PCB Boards", style={
                                'margin-bottom': '10px', 'margin-top': '15px'}),
                        dbc.Table(bordered=True,
                                  id='display-selected-values')
                    ]), width=8
                ),
            ]
        ),
    ], style={'padding': '40px'}
)

pinPlotDiv = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id='Graph1',
                            figure=pin_plot,
                            style={'margin': '40px'}
                        )
                    ], width=12
                ),
            ]
        ),
    ],
    className="mt-10", style={'margin-right': 'auto', 'margin-left': 'auto'}
)

correlationDiv = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id='Graph2',
                            figure=correlation_plot
                        ),
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id='Graph3',
                            figure=correlation_plot_clustering
                        ),
                    ]
                ),
            ]
        )
    ],
    className="mt-4",
)

dash_app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Indivudal Tool Accuracy Assessment', value='tab-1'),
        dcc.Tab(label='Connector Position Plot', value='tab-2'),
        dcc.Tab(label='Correlation Matrix', value='tab-3'),

    ], style={'font-size':'12px', 'padding':'3px'}),
    html.Div(id='tabs-content', children=html.Div([toolDiv]))
])

@dash_app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([toolDiv])
    elif tab == 'tab-2':
        return html.Div([pinPlotDiv])
    elif tab == 'tab-3':
        return html.Div([correlationDiv])


@dash_app.callback(
    Output('cities-dropdown', 'options'),
    [Input('countries-dropdown', 'value')])
def set_tool_options(selected_tool_cat):
    return [{'label': i, 'value': i} for i in toolData[selected_tool_cat]]


@dash_app.callback(
    Output('cities-dropdown', 'value'),
    [Input('cities-dropdown', 'options')])
def set_tool_ids(available_tools):
    return available_tools[0]['value']


@dash_app.callback(
    [Output('display-selected-values', 'children'),
     Output('tool_deviation', 'children'),
     Output('tool_cat', 'children'),
     Output('tool_id', 'children')],
    [Input('countries-dropdown', 'value'),
     Input('cities-dropdown', 'value')])
def set_display_children(selected_tool_cat, selected_tool):
    table_header = [
        html.Thead(html.Tr([html.Th("PCB Board"), html.Th("Deviation")]))
    ]
    rows = []
    for pcb_board in toolData[selected_tool_cat][selected_tool]['pcb_list']:
        rows.append(html.Tr([html.Td(pcb_board[0]), html.Td(pcb_board[1])]))

    table_body = [html.Tbody(rows)]
    return table_header + table_body, toolData[selected_tool_cat][selected_tool]['accuracy'], selected_tool_cat, selected_tool
def read_data(start='2019-03-01',end='2019-09-31'):
    data=pd.read_csv('data.csv')
    data=data[(data['Production Date']>start)&(data['Production Date']<end)]
    return data


# 创建一个服务，把当前这个python文件当做一个服务
# server = flask.Flask(__name__)
# dash_app=Dash(__name__,server=server,url_base_pathname='/dashboard/')
# dash_app.layout = html.Form(id='form',className='form',method="get",action="/api/upload" ,encType="multipart/form-data",children=[
#                        html.Div(children=[
#                            dcc.DatePickerSingle(date=dt(1997, 5, 10),id='start_date',className='start_date',persistence ='start_date'),
#                            dcc.DatePickerSingle(date=dt(1997, 5, 10), id='end_date', className='date'),
#                            html.Button('Submit', id='button',type="submit")])])


basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['csv'])



# 用于测试上传，稍后用到
@server.route('/upload')
def upload_test():
    return render_template('upload.html')




# 上传文件
@server.route('/api/upload', methods=['POST','get'], strict_slashes=False)
def api_upload():
        start= request.values.get('date') # 从表单的file字段获取文件，myfile为该表单的name值
        end =request.values.get('end_date')
        data = read_data(start=start, end=end)  # ld.load_data(start_date=start,).load_data()
        if data.shape[0] != 0:
            result = pp.ProfileReport(data)
            return result.to_html()
        else:
            return json.dumps({start:'empty data'})
# @server.route()可以将普通函数转变为服务 登录接口的路径、请求方式
@server.route('/result', methods=['get', 'post'])
def run():
    # 获取通过url请求传参的数据 sql
    start= request.values.get('start')
    end=request.values.get('end')
    data =read_data(start=start, end=end)
    if data.shape[0]!=0:
      result=pp.ProfileReport(data)
      return result.to_html()
    else:
        return json.dump({'err type': 'empty data'})

if __name__ == '__main__':
    dash_app.run_server(debug=True, port=8898)
