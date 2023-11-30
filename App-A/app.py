import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from PIL import Image

huw_image = Image.open("data/huawei-logo.png")
mob_image = Image.open("data/mobily.png")

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])
server = app.server

sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    vertical=False,
    pills=True,
    className="bg-light custom-sidebar",
)

app.layout = html.Div([
    dbc.Container(
        [
            dbc.Row([
                dbc.Col(
                    dbc.Col([
                        html.Div([
                            html.Img(src=huw_image, style={'height': '50px', 'width': '50px'}),
                            html.Img(src=mob_image, style={'height': '50px', 'width': '100px'}),
                            html.H1("South Region Performance Dashboard", className='text-center', style={'fontSize': 50, 'color': 'white'}),
                        ],
                            className='d-flex justify-content-center align-items-center',
                            style={'backgroundColor': '#4771a0'}
                        )
                    ])
                )
            ]),
            html.Hr(),
            dbc.Row([sidebar]),
            dbc.Row([dash.page_container])
        ],
        fluid=True
    )
])

if __name__ == "__main__":
    app.run(debug=False)
