from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

data = pd.read_csv('Oil and Gas 1932-2014.csv')
data.head()
data.info()

app = Dash()

app.layout = html.Div([
    html.H1(children='Oil and Gas 1932-2014', style={'textAlign':'center'}),
    html.H3(children='Select a country:'),
    dcc.Dropdown(data.cty_name.unique(), 'Canada', id='dropdown-selection'),
    # slider for year
    html.H3(id='slider-year-output'),
    dcc.Slider(
        min=data.year.min(), 
        max=data.year.max(), 
        value=data.year.min(), 
        marks={str(data.year.min()): str(data.year.min()), str(data.year.max()): str(data.year.max())}, 
        step=1, 
        id='slider-year',
        tooltip={
            "always_visible": False,
            "style": {"color": "LightSteelBlue", "fontSize": "20px"},
        },
    ),
    dcc.Graph(id='graph-timeseries'),
    dcc.Graph(id='graph-map'),
], style={'fontSize': 24, 'fontFamily': 'Arial'})

@callback(
    Output('graph-timeseries', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dataf = data[data.cty_name == value]
    fig = px.line()
    fig.update_layout(xaxis_title='Year', yaxis_title='Population')
    # add leyend title and population
    fig.update_layout(legend_title_text='Population')

    # dual axis
    fig.add_scatter(x=dataf.year, y=dataf.gas_value_2014, mode='lines', name='Gas Production', yaxis='y2')
    fig.add_scatter(x=dataf.year, y=dataf.oil_value_2014, mode='lines', name='Oil Production', yaxis='y2')
    fig.add_scatter(x=dataf.year, y=dataf.population, mode='lines', name='Population')

    # Create secondary y-axis
    fig.update_layout(
        yaxis2=dict(
            title='Oil & Gas Production',
            overlaying='y',
            side='right'
        ),
        yaxis=dict(
            title='Population'
        ),
        # move the legend to the top
        legend=dict(
            yanchor='top',
            y=0.99,
            xanchor='left',
            x=0.01
        )
    )

    return fig

@callback(
    Output('graph-map', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('slider-year', 'value')
)
def update_map(value, year):
    dataf = data[(data.cty_name == value) & (data.year == year)]
    return px.choropleth(
        dataf, 
        locations="cty_name", 
        locationmode="country names", 
        color="cty_name", 
        hover_name="cty_name",
        hover_data={"population": True, "year": True},
        projection="natural earth", 
        title=f"Population of {value} in {year}",
        # legend title
        labels={'cty_name': 'Country', 'population': 'Population', 'year': 'Year'}
            )

if __name__ == '__main__':
    app.run(debug=True)
