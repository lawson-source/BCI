import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os

dirf=os.path.abspath(os.path.dirname(__file__)) # root directory

# read result
mat_result=pd.read_csv(dirf+'/result_data/mat_result.csv')
mould_result=pd.read_csv(dirf+'/result_data/mould_result.csv')
tool_result=pd.read_csv(dirf+'/result_data/tool_result.csv')
suggestion=pd.read_csv(dirf+'/combination_item.csv')
suggestion['confidence']=suggestion['n']/suggestion['N']
suggestion=suggestion[['item','confidence']].sort_values('confidence',ascending=False)

# Dash instantiation
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1,",'title':'bosch'}],
    index_string= """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>bosch</title>
        {%favicon%}
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
server = app.server

#bulid tabs
def build_tabs():
    return html.Div(
        id='tabs',
        className='tabs',
        children=[
            dcc.Tabs(
                id='app-tabs',
                value='tab4',
                className='custom-tabs',
                children=[

                    dcc.Tab(
                        id='mat-tab',
                        label='matDataBComponents',
                        value='tab2',
                        className='custom-tab',
                        selected_className='custom-tab--selected',
                        children=[
                            dcc.Graph(id='bad-my-div2', figure=dict({
                                "data": [
                                    {
                                        "x": mat_result['item1'].str.replace(u'frozenset\\({', '').str.replace('vendor',
                                                                                                               'V').str.replace(
                                            'MouldMachineNo', 'MMN').str.replace('matDataBComponents',
                                                                                 'MDC').str.replace('toolData',
                                                                                                    'TD').str.strip(
                                            u'\\})'),
                                        "y": mat_result['support'],
                                        "type": "bar",
                                        'name': 'support',

                                    },
                                    {
                                        "x": mat_result['item1'].str.replace(u'frozenset\\({', '').str.replace('vendor',
                                                                                                               'V').str.replace(
                                            'MouldMachineNo', 'MMN').str.replace('matDataBComponents',
                                                                                 'MDC').str.replace('toolData',
                                                                                                    'TD').str.strip(
                                            u'\\})'),
                                        "y": mat_result['confidence'],
                                        "type": "bar",
                                        'name': 'confidence',
                                    },
                                    {
                                        "x": mat_result['item1'].str.replace(u'frozenset\\({', '').str.replace('vendor',
                                                                                                               'V').str.replace(
                                            'MouldMachineNo', 'MMN').str.replace('matDataBComponents',
                                                                                 'MDC').str.replace('toolData',
                                                                                                    'TD').str.strip(
                                            u'\\})'),
                                        "y": mat_result['lift'],
                                        "type": "bar",
                                        'name': 'lift',
                                    }
                                ],
                                'layout':
                                    {
                                        "title": 'Association Support',
                                        "paper_bgcolor": "rgba(0,0,0,0)",
                                        "plot_bgcolor": "rgba(0,0,0,0)",
                                        "font": {"color": "white"},
                                        "autosize": True,

                                    }

                            }, ))
                        ]
                    ),
                    dcc.Tab(
                        id='Mou-tab',
                        label='Moulding',
                        value='tab3',
                        className='custom-tab',
                        selected_className='custom-tab--selected',
                        children=[
                            dcc.Graph(id='bad-my-div3', figure=dict({
                                "data": [
                                    {
                                        "x": mould_result['item1'].str.replace(u'frozenset\\({', '').str.replace('MouldMachineNo',
                                                                                                               'MMN').str.replace(
                                            'Moulding.toolData', 'MTD').str.replace('MouldNestNo',
                                                                                 'MNN').str.replace('.toolID','').str.strip(
                                            u'\\})'),
                                        "y": mould_result['support'],
                                        "type": "bar",
                                        'name': 'support',

                                    },
                                    {
                                        "x": mould_result['item1'].str.replace(u'frozenset\\({', '').str.replace('MouldMachineNo',
                                                                                                               'MMN').str.replace(
                                            'Moulding.toolData', 'MTD').str.replace('MouldNestNo',
                                                                                 'MNN').str.replace('.toolID','').str.strip(
                                            u'\\})'),
                                        "y": mould_result['confidence'],
                                        "type": "bar",
                                        'name': 'confidence',
                                    },
                                    {
                                        "x": mould_result['item1'].str.replace(u'frozenset\\({', '').str.replace('MouldMachineNo',
                                                                                                               'MMN').str.replace(
                                            'Moulding.toolData', 'MTD').str.replace('MouldNestNo',
                                                                                 'MNN').str.replace('.toolID','').str.strip(
                                            u'\\})'),
                                        "y": mould_result['lift'],
                                        "type": "bar",
                                        'name': 'lift',
                                    }
                                ],
                                'layout':
                                    {
                                        "title": 'Association Support',
                                        "paper_bgcolor": "rgba(0,0,0,0)",
                                        "plot_bgcolor": "rgba(0,0,0,0)",
                                        "font": {"color": "white"},
                                        "autosize": True,



                                    }

                            }, ))
                        ]
                    ),
                    dcc.Tab(
                        id='too-tab',
                        label='toolData',
                        value='tab4',
                        className='custom-tab',
                        selected_className='custom-tab--selected',
                        children=[
                            dcc.Graph(id='bad-my-div4', figure=dict({
                                "data": [
                                    {
                                        "x": tool_result['item1'].str.replace(u'frozenset\\({', '').str.replace('vendor',
                                                                                                               'V').str.replace(
                                            'MouldMachineNo', 'MMN').str.replace('matDataBComponents',
                                                                                 'MDC').str.replace('toolData',
                                                                                                    'TD').str.strip(
                                            u'\\})'),
                                        "y": tool_result['support'],
                                        "type": "bar",
                                        'name': 'support',

                                    },
                                    {
                                        "x": tool_result['item1'].str.replace(u'frozenset\\({', '').str.replace('vendor',
                                                                                                               'V').str.replace(
                                            'MouldMachineNo', 'MMN').str.replace('matDataBComponents',
                                                                                 'MDC').str.replace('toolData',
                                                                                                    'TD').str.strip(
                                            u'\\})'),
                                        "y": tool_result['confidence'],
                                        "type": "bar",
                                        'name': 'confidence',
                                    },
                                    {
                                        "x": tool_result['item1'].str.replace(u'frozenset\\({', '').str.replace('vendor',
                                                                                                               'V').str.replace(
                                            'MouldMachineNo', 'MMN').str.replace('matDataBComponents',
                                                                                 'MDC').str.replace('toolData',
                                                                                                    'TD').str.strip(
                                            u'\\})'),
                                        "y": tool_result['lift'],
                                        "type": "bar",
                                        'name': 'lift',
                                    }
                                ],
                                'layout':
                                    {
                                        "title": 'Association Support',
                                        "paper_bgcolor": "rgba(0,0,0,0)",
                                        "plot_bgcolor": "rgba(0,0,0,0)",
                                        "font": {"color": "white"},
                                        "autosize": True,

                                    }

                            }, ))
                        ]
                    ),

                ]


            )
        ]

    )

# build website title
def build_banner():
    return html.Div(
        id="banner",style=dict(width='90%'),
        className="banner",
        children=[
            html.Div(
                id="banner-logo",
                children=[
                    html.Div(
                    html.Img(id="logo", src=app.get_asset_url("bosch logo.png"))
                    ),
                    html.Div(
                        id="banner-text",
                        children=[
                            html.H5("BOSCH manufacture"),
                            html.H6("Process Status"),
                        ],
                    ),
                ],
            ),


        ],
    )

def create_table(df, max_rows=10):
    """基于dataframe，设置表格格式"""

    table = html.Table(style=dict(width='100%'),
        children=[
            html.Tr(
                [
                    html.Th(col) for col in df.columns
                ]
            )
        ] +
        # Body
        [
            html.Tr(
                [
                    html.Td(
                        df.iloc[i][col]
                    ) for col in df.columns
                ]
            ) for i in range(min(len(df), max_rows))
        ]
    )
    return table
# display output
app.layout = html.Div(
    children= [
                    build_banner(),
                    build_tabs(),
        create_table(suggestion)

                    ]
    )



if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
