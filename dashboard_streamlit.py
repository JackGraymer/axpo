import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# Title
st.title('AXPO - Petroleum / Oil Desk Dashboard')
st.sidebar.title('Dashboard Control Panel')

### Reading excel file and preparing data

#read excel file xls tab 2
xls = pd.ExcelFile('data/RBRTEd.xls')
# print(xls.sheet_names)
brent = xls.parse('Data 1', skiprows=2) #skip first 2 rows
#brent.head()
brent.columns = ['date', 'brent_price'] #rename columns

xls = pd.ExcelFile('data/RWTCd.xls')
# print(xls.sheet_names)
wti = xls.parse('Data 1', skiprows=2) #skip first 2 rows
#wti.head()
wti.columns = ['date', 'wti_price'] #rename columns

# merge brent and wti dataframes
wti_brent = pd.merge(brent, wti, on='date', how='inner')

### Creating time stamps for filter buttons
# last month
last_month = wti_brent.iloc[-30:]

# last 3 months
last_3_months = wti_brent.iloc[-90:]

# last 6 months
last_6_months = wti_brent.iloc[-180:]

# last year
last_year = wti_brent.iloc[-365:]

# last 5 years
last_5_years = wti_brent.iloc[-1825:]

# all time
all_time = wti_brent

# add buttons for the last month, 3 months, 6 months, last year, last 5 years and all time
st.header('Brent and WTI Prices')
period = st.segmented_control('Period:', ['Last Month', 'Last 3 Months', 'Last 6 Months', 'Last Year', 'Last 5 Years', "All Time"], selection_mode="single", default='Last Month')

period_dict = {
    'Last Month': last_month,
    'Last 3 Months': last_3_months,
    'Last 6 Months': last_6_months,
    'Last Year': last_year,
    'Last 5 Years': last_5_years,
    'All Time': all_time
}

# plot is filtered by the period selected by the user in the segmented control widget
df = ""
#if period not in period_dict: then df = all_time
if period not in period_dict: # this is necessary to avoid KeyError (Streamlit has not implemented a required value for the segmented control)
    period = 'All Time'
    df = period_dict[period]
else:
    df = period_dict[period]

# create a line plot using plotly go.Figure
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.date, y=df.brent_price, mode='lines', name='Brent Price'))
fig.add_trace(go.Scatter(x=df.date, y=df.wti_price, mode='lines', name='WTI Price'))
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Price',
    legend_title_text='Price',
    legend=dict(x=0, y=1),
    title=f'Brent and WTI Prices in the {period}'
)
st.plotly_chart(fig)

# create a line plot using plotly express (same as above)
#variable "_" is used to avoid printing commented code
_="""fig = px.line(df, x='date', y=['brent_price', 'wti_price'], labels={'value': 'Price', 'variable': 'Type'}, title=f'Brent and WTI Prices in the {period}')
fig.update_layout(legend_title_text='Price', legend=dict(x=0, y=1))

# change leyend names for brent and wti
fig.update_traces(name='Brent Price', selector=dict(name='brent_price'))
fig.update_traces(name='WTI Price', selector=dict(name='wti_price'))

st.plotly_chart(fig)
"""

### STOCKS ###

# read files
apple = pd.read_csv('data/AAPL.csv')

tesla = pd.read_csv('data/Tesla.csv')
tesla['Date'] = pd.to_datetime(tesla['Date'])

microsoft = pd.read_csv('data/MicrosoftStock.csv')
#change column names 
microsoft.columns = ['Index', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Name']
microsoft = microsoft.drop(columns=['Index', 'Volume','Name'])

# create buttons for Apple, Tesla and Microsoft
st.sidebar.header('Stock Prices')
stock = st.sidebar.radio('Select a stock:', ['Apple', 'Tesla', 'Microsoft'])

# Select the appropriate DataFrame based on the selected stock
if stock == 'Apple':
    selected_stock = apple
elif stock == 'Tesla':
    selected_stock = tesla
else:
    selected_stock = microsoft
selected_stock = selected_stock.iloc[-1000:] # last 1000 days

# candlestick chart
fig_stock = go.Figure(data=[go.Candlestick(x=selected_stock['Date'],
                open=selected_stock['Open'],
                high=selected_stock['High'],
                low=selected_stock['Low'],
                close=selected_stock['Close'])])

fig_stock.update_layout(
    title=f'{stock} Stock Prices',
    xaxis_title='Date',
    yaxis_title='Price',
    legend_title_text='Price',
    legend=dict(x=0, y=1),
    xaxis_rangeslider_visible=False
)

st.header(f'{stock} Stock Prices')
st.plotly_chart(fig_stock, key=stock)

# sidebar add a separator line ---
st.sidebar.markdown('---')

### OIL AND GAS ###

# 2. Reading excel file and preparing data

data = pd.read_csv('data/Oil and Gas 1932-2014.csv')
data.head()
#data.info()

# initialize the app
st.header('Oil and Gas 1932-2014')

# change maximun width for wider display
st.markdown(""" <style> .stMainBlockContainer {max-width: 1080px;} </style> """, unsafe_allow_html=True)

# sidebar
st.sidebar.title('Oil and Gas 1932-2014')
st.sidebar.write('Select a country and year to see the population, oil and gas production')

# select a country in the sidebar

st.sidebar.header('Select a country:')
country = st.sidebar.selectbox('Country:', data.cty_name.unique())
data_cty = data[data.cty_name == country]

# slider for year in the sidebar
st.sidebar.header('Select a year:')
year = st.sidebar.slider('Year:', min_value=data.year.min(), max_value=data.year.max(), value=data.year.min(), step=1)
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

# create a map plot
fig2 = px.choropleth(data_cty_year,
        locations="cty_name", 
        locationmode="country names", 
        color="cty_name", 
        hover_name="cty_name",
        hover_data={"population": True, "year": True},
        projection="natural earth", 
        title=f"Population by Country: {country} in {year}",
)
container1 = st.container()
col1, col2 = st.columns(2)
with container1:
    with col1:
        st.plotly_chart(fig)
    with col2 :
        st.plotly_chart(fig2)

### iris dataset ###

iris = px.data.iris()
st.header('Iris Dataset')
st.write('This is the Iris dataset from Plotly Express')

# donut chart of number of species
st.plotly_chart(px.pie(iris, names='species', hole=0.6, title='Number of Species', hover_data={'species': True}))

# scatter plot of petal width vs sepal length
petal = px.scatter(iris, x='petal_width', y='petal_length', color='species', hover_data=['petal_width', 'petal_length'], color_discrete_sequence=px.colors.qualitative.G10,)

# scatter plot of sepal width vs sepal length
sepal = px.scatter(iris, x='sepal_width', y='sepal_length', color='species', hover_data=['petal_width', 'petal_length'], color_discrete_sequence=px.colors.qualitative.G10,)

# create a 2 column layout for the scatter plots
container2 = st.container()
col3, col4 = st.columns(2)
with container2:
    with col3:
        st.plotly_chart(petal)

    with col4:
        st.plotly_chart(sepal)


# Sample DataFrame
data = {
    'Column1': [f'Row {i}' for i in range(1, 51)],
    'Column2': [i * 10 for i in range(1, 51)],
    'Column3': [i * 100 for i in range(1, 51)]
}
df = pd.DataFrame(data)

