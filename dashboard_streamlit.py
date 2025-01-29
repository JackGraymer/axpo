import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

data = pd.read_csv('data/Oil and Gas 1932-2014.csv')
data.head()
data.info()

# initialize the app

st.title('Oil and Gas 1932-2014')

# select a country

st.header('Select a country:')
country = st.selectbox('Country:', data.cty_name.unique())
data_cty = data[data.cty_name == country]
# slider for year

st.header('Select a year:')
year = st.slider('Year:', min_value=data.year.min(), max_value=data.year.max(), value=data.year.min(), step=1)
data_year = data[data.year == year]

data_cty_year = data[(data.cty_name == country) & (data.year == year)]
# create a timeseries plot

data_cty = data[data.cty_name == country]
fig = go.Figure()
fig.add_trace(go.Scatter(x=data_cty.year, y=data_cty.gas_value_2014, mode='lines', name='Gas Production', yaxis='y2'))
fig.add_trace(go.Scatter(x=data_cty.year, y=data_cty.oil_value_2014, mode='lines', name='Oil Production', yaxis='y2'))
fig.add_trace(go.Scatter(x=data_cty.year, y=data_cty.population, mode='lines', name='Population'))
fig.update_layout(xaxis_title='Year', yaxis_title='Population')
fig.update_layout(legend_title_text='Population', legend=dict(x=0, y=1))
fig.update_layout(
    yaxis2=dict(
        title='Oil & Gas Production',
        overlaying='y',
        side='right'
    ),
    yaxis=dict(
        title='Population'
    ),
    title=f"Population, Oil & GasProduction by Country: {country} in {year}",
)

st.plotly_chart(fig)

# create a map plot
fig = px.choropleth(data_cty_year,
        locations="cty_name", 
        locationmode="country names", 
        color="cty_name", 
        hover_name="cty_name",
        hover_data={"population": True, "year": True},
        projection="natural earth", 
        title=f"Population by Country: {country} in {year}",
)

st.plotly_chart(fig)
# create a table


