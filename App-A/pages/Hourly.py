import dash
from dash import dcc, html, callback, Input, Output
from dash_core_components import Tabs
#from dash.dependencies import Input, Output
import plotly.express as px
#from dash_page import DashPage
import pandas as pd
from datetime import datetime, timedelta  # Import datetime module

#from main import app  # Import the 'app' object from the main file

dash.register_page(__name__)
# Define the dataframes for the second page
df_4G_h = pd.read_csv("data/4G_h.csv")
df_5G_h = pd.read_csv("data/5G_h.csv")
df_3G_h = pd.read_csv("data/3G_h.csv")
df_2G_h = pd.read_csv("data/2G_h.csv")
df_volte_h = pd.read_csv("data/Volte_h.csv")
df_iot_h = pd.read_csv("data/IOT_h.csv")


df_4G_h['Date'] = pd.to_datetime(df_4G_h['Date']).dt.strftime('%Y-%m-%d')
df_4G_h['Time'] = pd.to_datetime(df_4G_h['Time'])
df_4G_h['Time'] = df_4G_h['Time'].dt.strftime('%H:%M:%S')
df_4G_h.set_index('Date', inplace=True)


df_5G_h['Date'] = pd.to_datetime(df_5G_h['Date']).dt.strftime('%Y-%m-%d')
df_5G_h['Time'] = pd.to_datetime(df_5G_h['Time'])
df_5G_h['Time'] = df_5G_h['Time'].dt.strftime('%H:%M:%S')
df_5G_h.set_index('Date', inplace=True)

df_3G_h['Date'] = pd.to_datetime(df_3G_h['Date']).dt.strftime('%Y-%m-%d')
df_3G_h['Time'] = pd.to_datetime(df_3G_h['Time'])
df_3G_h['Time'] = df_3G_h['Time'].dt.strftime('%H:%M:%S')
df_3G_h.set_index('Date', inplace=True)

df_2G_h['Date'] = pd.to_datetime(df_2G_h['Date']).dt.strftime('%Y-%m-%d')
df_2G_h['Time'] = pd.to_datetime(df_2G_h['Time'])
df_2G_h['Time'] = df_2G_h['Time'].dt.strftime('%H:%M:%S')
df_2G_h.set_index('Date', inplace=True)

df_volte_h['Date'] = pd.to_datetime(df_volte_h['Date']).dt.strftime('%Y-%m-%d')
df_volte_h['Time'] = pd.to_datetime(df_volte_h['Time'])
df_volte_h['Time'] = df_volte_h['Time'].dt.strftime('%H:%M:%S')
df_volte_h.set_index('Date', inplace=True)

df_iot_h['Date'] = pd.to_datetime(df_iot_h['Date']).dt.strftime('%Y-%m-%d')
df_iot_h['Time'] = pd.to_datetime(df_iot_h['Time'])
df_iot_h['Time'] = df_iot_h['Time'].dt.strftime('%H:%M:%S')
df_iot_h.set_index('Date', inplace=True)

today = datetime.now().date()
yesterday = today - timedelta(days=1)
last_week = today - timedelta(weeks=1)

start_date_default = last_week
end_date_default = today

layout = html.Div(
    [
        html.H1("Hourly Performance Dashboard", style={'textAlign': 'center', 'fontSize': 30}),
        html.Label("Select Cluster", style={'fontSize': 20}),
    #Dropdown for selecting category
        dcc.Dropdown(id='category-dropdown_h', multi=False, style={'width': '50%'}, value=df_4G_h.iloc[:, 1].unique()[0]),
    # Date range picker
        dcc.DatePickerRange(
            id='date-picker-range_h',
            start_date=start_date_default,
            end_date=end_date_default,
            display_format='YYYY-MM-DD',
        ),
    # Tabs for 4G and 5G Data
        dcc.Tabs(id= 'tabs_h', value='tab-4G_h', children=[
        dcc.Tab(label='4G Data', value='tab-4G_h'),
        dcc.Tab(label='5G Data', value='tab-5G_h'),
        dcc.Tab(label='Volte Data', value='tab-Volte_h'),
        dcc.Tab(label='3G Data', value='tab-3G_h'),
        dcc.Tab(label='2G Data', value='tab-2G_h'),
        dcc.Tab(label='IOT Data', value='tab-IOT_h'),
    ]),
        html.Div(
        [
            # Wrap your charts in dcc.Loading component
            dcc.Loading(
                id="loading-charts_h",
                type="circle",  # other types include "default", "circle", "dot", "default"
                children=[
                    html.Div(id='charts-container_h', style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'}),
                ]
            )
        ],
        style={'padding': '20px'})

    #tml.Div(id='charts-container_h', style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'}),
    ])
#Callback to update category dropdown and date picker based on selected tab
@callback(
    [Output('category-dropdown_h', 'options'),
     Output('date-picker-range_h', 'start_date'),
     Output('date-picker-range_h', 'end_date')],
    [Input('tabs_h', 'value')]
)
def update_category_dropdown_options(selected_tab):
    print(f'Selected Tab: {selected_tab}')

    if selected_tab == 'tab-4G_h':
        df_h = df_4G_h
    elif selected_tab == 'tab-5G_h':
        df_h = df_5G_h
    elif selected_tab == 'tab-Volte_h':
        df_h = df_volte_h
    elif selected_tab == 'tab-3G_h':
        df_h = df_3G_h
    elif selected_tab == 'tab-2G_h':
        df_h = df_2G_h
    elif selected_tab == 'tab-IOT_h':
        df_h = df_iot_h

    #print(df_h.iloc[:, 1].unique())
    categories =  [x for x in df_h.iloc[:, 1].unique()]


    #categories = [x for x in df_h.iloc[:,1].unique()]

    # Update date range picker values
    start_date = df_h.index.min()
    end_date = df_h.index.max()
    return [{'label': category, 'value': category} for category in categories], start_date, end_date


    #return categories, start_date, end_date


# Callback to update charts based on user input
@callback(
    Output('charts-container_h', 'children'),
    [Input('tabs_h', 'value'),
     Input('category-dropdown_h', 'value'),
     Input('date-picker-range_h', 'start_date'),
     Input('date-picker-range_h', 'end_date')]
)
def update_charts(selected_tab, selected_categories, start_date, end_date):
    if selected_tab == 'tab-4G_h':
        dataframe_h = df_4G_h
    elif selected_tab == 'tab-5G_h':
        dataframe_h = df_5G_h
    elif selected_tab == 'tab-Volte_h':
        dataframe_h = df_volte_h
    elif selected_tab == 'tab-3G_h':
        dataframe_h = df_3G_h
    elif selected_tab == 'tab-2G_h':
        dataframe_h = df_2G_h
    elif selected_tab == 'tab-IOT_h':
        dataframe_h = df_iot_h

    # Convert selected_categories to a list of values if it is not None
    if selected_categories is None:
        selected_categories_list = []
    else:
        selected_categories_list = selected_categories if isinstance(selected_categories, list) else [selected_categories]
    #selected_categories_list = selected_categories if selected_categories else [default_category]

    filtered_df_h = dataframe_h[(dataframe_h.iloc[:,1].isin(selected_categories_list)) & (dataframe_h.index >= start_date) & (dataframe_h.index <= end_date)]


    numerical_columns = filtered_df_h.columns[3:]
    filtered_df_h = filtered_df_h.reset_index()



# Generate charts dynamically

    charts = []
    for column in numerical_columns:
        fig = px.line(filtered_df_h, x='Time', y=column, color='Date',
                      labels={'Time': 'Time', column: f'{column}'},
                      template='ggplot2',
                      height=400,
                      width=600)

        # Customize legend
        fig.update_layout(legend=dict(title='', orientation='h', y=1.3), 
                            yaxis_title={
                'text': f'<b>{column}</b>',
                'font': {'size': 16, 'family': 'Arial, sans-serif', 'color': 'black'},
            },)

        
        # Exclude undesired dates from the x-axis
        # for trace in fig.data:
        #     if 'x' in trace:
        #         trace.update(x=[val for val in trace['x'] if val not in undesired_dates])

        chart = dcc.Graph(id=f'chart-{column}', figure=fig)
        charts.append(html.Div(chart, style={'width': '30%', 'padding': '5px', 'margin': 'auto'}))

    return charts
