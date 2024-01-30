import os

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html

try:
    debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
except:
    debug = True

external_stylesheets = [dbc.themes.YETI]

app = Dash(__name__,
           use_pages=True,
           external_stylesheets=external_stylesheets,
           meta_tags=[
               {"name": "viewport", "content": "width=device-width, initial-scale=1"},
           ],
           suppress_callback_exceptions=True)
app.title = "Big DB"

server = app.server


def serve_layout():
    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=dash.get_asset_url('microingranaggi_logo.jpg'), height="60px")),
                            dbc.Col(dbc.NavbarBrand(f"BigDB {'- Versione di sviluppo' if debug else ''}"
                                                    , className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href=dash.page_registry['pages.home']["relative_path"],
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)
            ]
        ),
        color="dark",
        dark=True,
    )
    return html.Div(children=[
        navbar,
        html.Br(),
        html.Div(
            className="container",
            children=[
                dash.page_container
            ]
        )
    ])


app.layout = serve_layout

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=debug, threaded=True)
