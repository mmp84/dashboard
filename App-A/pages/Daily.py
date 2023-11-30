import dash
from dash import dcc, html, callback, Output, Input
from dash.exceptions import PreventUpdate
from dash_core_components import Tabs
import plotly.express as px
import pandas as pd
from PIL import Image
from dash_html_components import Img

dash.register_page(__name__, path='/', description='Daily charts.', title='Daily',)

df_4G = pd.read_csv("data/4G.csv")
df_5G = pd.read_csv("data/5G.csv")
df_volte = pd.read_csv("data/Volte.csv")
df_3G = pd.read_csv("data/3G.csv")
df_2G = pd.read_csv("data/2G.csv")
df_iot = pd.read_csv("data/IOT.csv")

df_4G['Date'] = pd.to_datetime(df_4G['Date'])
df_4G.set_index('Date', inplace=True)

df_5G['Date'] = pd.to_datetime(df_5G['Date'])
df_5G.set_index('Date', inplace=True)

df_volte['Date'] = pd.to_datetime(df_volte['Date'])
df_volte.set_index('Date', inplace=True)

df_3G['Date'] = pd.to_datetime(df_3G['Date'])
df_3G.set_index('Date', inplace=True)

df_2G['Date'] = pd.to_datetime(df_2G['Date'])
df_2G.set_index('Date', inplace=True)

df_iot['Date'] = pd.to_datetime(df_iot['Date'])
df_iot.set_index('Date', inplace=True)
df_2G.head()

# Layout of the page
layout = html.Div([
    # html.Img(src='https://github.com/mmp84/dashboard/blob/main/huawei.png', style={'width': 'auto', 'height': 'auto'}),

    html.H1("Daily Performance Dashboard", style={'textAlign': 'center', 'fontSize': 30}),

    html.Label("Select Cluster", style={'fontSize': 20}),
    # Dropdown for selecting category
    dcc.Dropdown(
        id='category-dropdown',
        multi=True,
        value=[df_4G.iloc[:, 0].unique()[0]],
        style={'width': '50%'},  # Set the default value to the first category in df_4G
    ),

    # Date range picker
    dcc.DatePickerRange(
        id='date-picker-range',
    ),

    # Tabs for 4G and 5G Data
    dcc.Tabs(id='tabs', value='tab-4G', children=[
        dcc.Tab(label='4G Data', value='tab-4G'),
        dcc.Tab(label='5G Data', value='tab-5G'),
        dcc.Tab(label='Volte Data', value='tab-Volte'),
        dcc.Tab(label='3G Data', value='tab-3G'),
        dcc.Tab(label='2G Data', value='tab-2G'),
        dcc.Tab(label='IOT Data', value='tab-IOT'),
    ]),

    # Dynamically generated charts in a grid layout

    html.Div(
        [
            # Wrap your charts in dcc.Loading component
            dcc.Loading(
                id="loading-charts",
                type="circle",  # other types include "default", "circle", "dot", "default"
                children=[
                    html.Div(id='charts-container', style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'}),
                ]
            )
        ],
        style={'padding': '20px'}
    ),

])

# Callback to update category dropdown and date picker based on selected tab
@callback(
    [Output('category-dropdown', 'options'),
     Output('date-picker-range', 'start_date'),
     Output('date-picker-range', 'end_date')],
    [Input('tabs', 'value')]
)
def update_category_dropdown_options(selected_tab):
    if selected_tab == 'tab-4G':
        df = df_4G
    elif selected_tab == 'tab-5G':
        df = df_5G
    elif selected_tab == 'tab-Volte':
        df = df_volte
    elif selected_tab == 'tab-3G':
        df = df_3G
    elif selected_tab == 'tab-2G':
        df = df_2G
    elif selected_tab == 'tab-IOT':
        df = df_iot

    # Update category dropdown options
    categories = [{'label': str(category), 'value': str(category)} for category in df.iloc[:, 0].unique()]
    categories = [category for category in categories if category['value'] is not None]

    # Update date range picker values
    start_date = df.index.min()
    end_date = df.index.max()

    return categories, start_date, end_date

# Callback to update charts based on user input
@callback(
    Output('charts-container', 'children'),
    [Input('tabs', 'value'),
     Input('category-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_charts(selected_tab, selected_categories, start_date, end_date):
    if selected_tab == 'tab-4G':
        dataframe = df_4G
    elif selected_tab == 'tab-5G':
        dataframe = df_5G
    elif selected_tab == 'tab-Volte':
        dataframe = df_volte
    elif selected_tab == 'tab-3G':
        dataframe = df_3G
    elif selected_tab == 'tab-2G':
        dataframe = df_2G
    elif selected_tab == 'tab-IOT':
        dataframe = df_iot

    # Convert selected_categories to a list of values if it is not None
    if selected_categories is None:
        selected_categories_list = []
    else:
        selected_categories_list = selected_categories if isinstance(selected_categories, list) else [selected_categories]

    filtered_df = dataframe[
        (dataframe.iloc[:, 0].isin(selected_categories_list)) & (dataframe.index >= start_date) & (
                    dataframe.index <= end_date)]
    # Generate charts dynamically
    charts = []
    for column in filtered_df.columns[2:]:
        fig = px.line(filtered_df, x=filtered_df.index, y=column, color=filtered_df.iloc[:, 0],
                      line_group=filtered_df.iloc[:, 0],
                      template='simple_white',
                      height=400,
                      width=600)  # Set an initial width in pixels

        # Customize legend
        fig.update_layout(
            title={
                'text': f'<b>{column}</b>',
                'font': {'size': 16, 'family': 'Arial, sans-serif', 'color': 'black'},
            },
            xaxis_title='Date',
            yaxis_title='',
            legend=dict(title='', orientation='h', y=1.1, x=0),
            font=dict(family='Arial, sans-serif', size=12, color='black'),  # Set font properties
            margin=dict(l=0, r=10, t=50, b=20),  # Set margins
            title_x=0.5,  # Center-align the title
            title_yanchor='bottom',  # Align the title at the top
            title_font=dict(size=16, family='Arial, sans-serif', color='black')  # Set title font properties
        )

        chart = dcc.Graph(id=f'chart-{column}', figure=fig)
        charts.append(
            html.Div(chart, style={'width': '30%', 'padding': '10px', 'margin': 'auto'}))  # Adjust width as needed

    # Arrange the charts in rows
    charts_container = html.Div(charts,
                                style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'})

    # Wrap your charts in dcc.Loading component
    loading_charts = dcc.Loading(
        id="loading-charts",
        type="circle",  # other types include "default", "circle", "dot", "default"
        children=[charts_container]
    )

    # Update the Output to use loading_charts
    return loading_charts

