# AXPO Dashboard

[Link to the dashboard](https://kbmma3xd8qkcucuzwqwvso.streamlit.app/)

This repository contains a Streamlit-based dashboard for visualizing petroleum/oil prices, stock prices, and historical oil and gas data. The dashboard provides interactive visualizations using Plotly and allows users to filter data by different time periods and select specific stocks or countries.

## Features

- **Petroleum/Oil Prices**: Visualize Brent and WTI prices over different time periods.
- **Stock Prices**: View candlestick charts for Apple, Tesla, and Microsoft stocks.
- **Oil and Gas Data**: Explore historical oil and gas production data by country and year.
- **Iris Dataset**: Display visualizations of the Iris dataset from Plotly Express.


## Data Sources

- **Brent and WTI Prices**: Excel files `RBRTEd.xls` and `RWTCd.xls` in the data directory.
- **Stock Prices**: CSV files `AAPL.csv`, `Tesla.csv`, and MicrosoftStock.csv in the data directory.
- **Oil and Gas Data**: CSV file `Oil and Gas 1932-2014.csv` in the data directory.

## Usage

### Petroleum/Oil Prices

1. Select the time period from the segmented control widget.
2. View the line plot of Brent and WTI prices for the selected period.

### Stock Prices

1. Select a stock (Apple, Tesla, or Microsoft) from the sidebar radio buttons.
2. View the candlestick chart for the selected stock.

### Oil and Gas Data

1. Select a country from the sidebar dropdown.
2. Select a year from the sidebar slider.
3. View the timeseries plot of population, oil, and gas production for the selected country and year.
4. View the map plot of population by country for the selected year.

### Iris Dataset

1. View the donut chart of the number of species.
2. View the scatter plots of petal width vs. sepal length and sepal width vs. sepal length.

## Requirements

Available in the `requirements.txt` file.

- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)