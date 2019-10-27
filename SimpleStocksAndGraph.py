import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime as dt
from glob import glob
import datetime


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker

    def gather_data(self):
        # block gets current date and sets appropriate variables
        d = datetime.datetime.today()
        year = d.year
        month = d.month
        day = d.day

        start = dt.datetime(2010, 1, 3)  # (YEAR, MONTH, DAY)
        end = dt.datetime(year, month, day)

        file = glob('tesla.csv')[0]

        df = web.DataReader(self.ticker, 'yahoo', start, end)
        df.to_csv(file)


class Graph:
    def __init__(self, stock_name):
        self.stock_name = stock_name

    def display_graph(self, df):
        # try to graph
        plt.style.use('dark_background')
        df[0]["Adj Close"].plot()
        plt.title(f"Stock Prices of {df[1]}")
        plt.ylabel("Price ($)")
        plt.show()
