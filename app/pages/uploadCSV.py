import io
import dash
import base64
import pandas as pd
import dash_bootstrap_components as dbc
from utils.csv_handler.csv_reader import insert_into_db
from dash import dcc, html, dash_table, Input, Output, State, callback, ctx

dash.register_page(__name__)

df = pd.DataFrame()

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
    global df
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8', errors='ignore')), on_bad_lines='skip', sep=';')
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

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=False,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=20,
            filter_options={"placeholder_text": "Filtro ..."}
        ),

        html.Hr(),

        html.Div([
            html.Div(
                [
                    dbc.Button("Upload", color="primary", id='uploadButton', n_clicks=0),
                ],
                className="d-grid gap-2",
            ),
            dcc.Loading(
                id="loading-2",
                children=[html.Div(id='container-button-timestamp')],
                type="circle",
            )
        ])
    ])


@callback(
    [Output('container-button-timestamp', 'children')],
    [Input('uploadButton', 'n_clicks')]
)
def display_click(n_clicks):
    if "uploadButton" == ctx.triggered_id:
        columns_list = df.columns.tolist()
        for row in df.values:
            row_df = pd.DataFrame(columns=columns_list, index=[0])
            row_df.loc[0] = row
            insert_into_db(row_df)
        return [html.H5("Dati Inseriti")]
    return [html.H5("")]


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
