import dash
from zipfile import ZipFile
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import os
basedir=os.path.abspath(os.path.dirname(__file__)) # root directory

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1,",'title':'bosch'}],
    index_string="""<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>bosch</title>
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%} 
        </footer>
    </body>
</html>"""
)
#service instantiatuon

app.layout=html.Div(
    children= [
                html.H2(children='please input the path'),
                dcc.Input(id='basedir',type="text",placeholder='please input the path',style={"margin" :"10px 0px 15px 5px",'width':'600px', 'height':'25px'}),
                html.H2(id='dropdown_text',children='please wait',style=dict(color='#EE0000')),
                dcc.Dropdown(id='dropdown1',),
                dcc.Graph(id='figure_PTC'),
                dcc.Graph(id='figure_SDC')

                    ]
    )
@app.callback([Output('dropdown1', 'options'),
               Output('dropdown_text', 'children'),
               Output('dropdown_text', 'style')
               ],
               [Input('basedir', 'value')])
def update_dropdown_1(File_dir):
        options = []
        Filelist_PTC = os.listdir(File_dir + '/Pneumatic Test Curve/')
        for File in Filelist_PTC:
            if ZipFile(File_dir + "/Pneumatic Test Curve/" + File).namelist().__contains__('P_Res2.csv'):
                options.append({'label': File, 'value': File})
                children='please select',
                style=dict(color='#000000')
        return options,children,style


@app.callback([Output('figure_PTC', 'figure'),
               Output('figure_SDC', 'figure')
               ],
              [Input('dropdown1', 'value'),
               Input('basedir', 'value')]
              )
def update_figure(option,File_dir):
    Filelist_SDC=os.listdir(File_dir+'\Staking Data_CSV2/')
    staking_name=File_dir+'\Staking Data_CSV2/'+[i for i in Filelist_SDC if option.split('_')[1] in i][0]
    data_2=pd.read_csv(staking_name,skiprows=32,sep=';',header=None,names=['x','y'])
    csv_file = ZipFile(File_dir + "/Pneumatic Test Curve/" + option).open('P_Res2.csv')
    data_1 = pd.read_csv(csv_file, sep=';', header=None, names=['x', 'y'])
    figure_PTC= dict(
        data=[dict(x=data_1['x'],
                   y=data_1['y'],
                   name=option,
                   marker=dict(
                       color='#EE0000'
                   )
        )],
        layout=dict(
            title='CC PTC chart',
            showlegend=True,
            legend=dict(x=0, y=1)

    ))
    figure_SDC=dict(
        data=[dict(x=data_2['x'],
                   y=data_2['y'],
                   name=[i for i in Filelist_SDC if option.split('_')[1] in i][0]
        )],
        layout=dict(
            title='CC SDC chart',
            showlegend=True,
            legend=dict(x=0, y=1)

    ))

    return figure_PTC,figure_SDC

if __name__ == '__main__':
    app.run_server(debug=False, port=8888)
