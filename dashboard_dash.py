import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, callback
from dash import Dash

# Initialize the app
app = Dash(__name__, suppress_callback_exceptions=True)

# Load the data
data = pd.read_csv('data/Oil and Gas 1932-2014.csv')

# Title
app.layout = html.Div([
    html.H1('AXPO - Petroleum / Oil Desk Dashboard', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.H3('Brent and WTI Prices'),
            dcc.Dropdown(
                id='period-dropdown',
                options=[
                    {'label': 'Last Month', 'value': 'Last Month'},
                    {'label': 'Last 3 Months', 'value': 'Last 3 Months'},
                    {'label': 'Last 6 Months', 'value': 'Last 6 Months'},
                    {'label': 'Last Year', 'value': 'Last Year'},
                    {'label': 'Last 5 Years', 'value': 'Last 5 Years'},
                    {'label': 'All Time', 'value': 'All Time'}
                ],
                value='Last Month'
            ),
            dcc.Graph(id='brent-wti-graph')
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            html.H3('Stock Prices'),
            dcc.RadioItems(
                id='stock-radio',
                options=[
                    {'label': 'Apple', 'value': 'Apple'},
                    {'label': 'Tesla', 'value': 'Tesla'},
                    {'label': 'Microsoft', 'value': 'Microsoft'}
                ],
                value='Apple'
            ),
            dcc.Graph(id='stock-graph')
        ], style={'width': '48%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    html.Div([
        html.Div([
            html.H3('Oil and Gas 1932-2014'),
            html.Label('Select Country'),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in data.cty_name.unique()],
                value='Canada'
            ),
            html.Br(),
            html.Label('Select Year'),
            dcc.Slider(
                id='year-slider',
                min=data.year.min(),
                max=data.year.max(),
                value=data.year.min(),
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
                step=1,
            ),
            dcc.Graph(id='oil-gas-graph'),
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='oil-gas-map')
        ], style={'width': '48%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    html.Div([
        html.Div([
            html.H3('Iris Dataset'),
            dcc.Graph(id='iris-donut', figure=px.pie(px.data.iris(), names='species', hole=0.6, title='Number of Species')),
        ], style={'width': '32%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='iris-petal', figure=px.scatter(px.data.iris(), x='petal_width', y='petal_length', color='species')),
        ], style={'width': '32%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='iris-sepal', figure=px.scatter(px.data.iris(), x='sepal_width', y='sepal_length', color='species'))
        ], style={'width': '32%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'})
], style={'padding': '20px', 'font-family': 'sans-serif'})

@app.callback(
    Output('brent-wti-graph', 'figure'),
    Input('period-dropdown', 'value')
)
def update_brent_wti_graph(period):
    xls = pd.ExcelFile('data/RBRTEd.xls')
    brent = xls.parse('Data 1', skiprows=2)
    brent.columns = ['date', 'brent_price']

    xls = pd.ExcelFile('data/RWTCd.xls')
    wti = xls.parse('Data 1', skiprows=2)
    wti.columns = ['date', 'wti_price']

    wti_brent = pd.merge(brent, wti, on='date', how='inner')

    period_dict = {
        'Last Month': wti_brent.iloc[-30:],
        'Last 3 Months': wti_brent.iloc[-90:],
        'Last 6 Months': wti_brent.iloc[-180:],
        'Last Year': wti_brent.iloc[-365:],
        'Last 5 Years': wti_brent.iloc[-1825:],
        'All Time': wti_brent
    }

    df = period_dict.get(period, wti_brent)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.date, y=df.brent_price, mode='lines', name='Brent Price'))
    fig.add_trace(go.Scatter(x=df.date, y=df.wti_price, mode='lines', name='WTI Price'))
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Price',
        legend_title_text='Price',
        title=f'Brent and WTI Prices in the {period}'
    )
    return fig

@app.callback(
    Output('stock-graph', 'figure'),
    Input('stock-radio', 'value')
)
def update_stock_graph(stock):
    if stock == 'Apple':
        selected_stock = pd.read_csv('data/AAPL.csv')
    elif stock == 'Tesla':
        selected_stock = pd.read_csv('data/Tesla.csv')
        selected_stock['Date'] = pd.to_datetime(selected_stock['Date'])
    else:
        selected_stock = pd.read_csv('data/MicrosoftStock.csv')
        selected_stock.columns = ['Index', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Name']
        selected_stock = selected_stock.drop(columns=['Index', 'Volume', 'Name'])

    selected_stock = selected_stock.iloc[-1000:]

    fig = go.Figure(data=[go.Candlestick(x=selected_stock['Date'],
                                         open=selected_stock['Open'],
                                         high=selected_stock['High'],
                                         low=selected_stock['Low'],
                                         close=selected_stock['Close'])])
    fig.update_layout(
        title=f'{stock} Stock Prices',
        xaxis_title='Date',
        yaxis_title='Price',
        legend_title_text='Price',
        xaxis_rangeslider_visible=False
    )
    return fig

@app.callback(
    Output('oil-gas-graph', 'figure'),
    Output('oil-gas-map', 'figure'),
    Input('country-dropdown', 'value'),
    Input('year-slider', 'value')
)
def update_oil_gas_graph(country, year):
    data_cty = data[data.cty_name == country]
    data_cty_year = data_cty[data_cty.year == year]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_cty.year, y=data_cty.gas_value_2014, mode='lines', name='Gas Production', yaxis='y2'))
    fig.add_trace(go.Scatter(x=data_cty.year, y=data_cty.oil_value_2014, mode='lines', name='Oil Production', yaxis='y2'))
    fig.add_trace(go.Scatter(x=data_cty.year, y=data_cty.population, mode='lines', name='Population'))
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Population',
        legend_title_text='Population',
        yaxis2=dict(
            title='Oil & Gas Production',
            overlaying='y',
            side='right'
        ),
        title=f"Population, Oil & Gas Production by Country: {country} in {year}",
        # legend position left top corner
        legend=dict(x=0, y=1)
    )

    fig2 = px.choropleth(data_cty_year,
                         locations="cty_name",
                         locationmode="country names",
                         color="cty_name",
                         hover_name="cty_name",
                         hover_data={"population": True, "year": True},
                         projection="natural earth",
                         title=f"Population by Country: {country} in {year}")
    return fig, fig2

if __name__ == '__main__':
    app.run(debug=True)
