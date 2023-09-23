import os
import io
import dash
import base64
import datetime
import pandas as pd
import plotly.express as px
from utils.db_connector import conn, query_homepage
from utils.csv_handler.csv_reader import read_csv
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback, ctx

dash.register_page(__name__)

layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        #html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            sort_action="native",
            sort_mode='multi',
            filter_action="native",
            filter_options={"placeholder_text": "Filter column..."},
            page_size=20
        ),

        html.Hr(),

        html.Div([
            html.Button('Upload', id='uploadButton', n_clicks=0),
            html.Div(id='container-button-timestamp')
        ])
    ])

@callback(
    Output('container-button-timestamp', 'children'),
    Input('uploadButton', 'n_clicks')
)

def displayClick(btn1):
    print("None of the buttons have been clicked yet")
    if "uploadButton" == ctx.triggered_id:
        return read_csv() #TODO: Passare DF e poi inserire i dati nelle tabelle :) 
    return html.H5("")

@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
              
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children