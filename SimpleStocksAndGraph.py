import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime as dt


def gatherData():
    start = dt.datetime(2018, 1, 3)  # (YEAR, MONTH, DAY)
    end = dt.datetime(2019, 10, 9)
    try:
        ticker = input("input ticker: ").upper()
        df = web.DataReader(ticker, 'yahoo', start, end)
        df.to_csv("test.csv")


        return df, ticker

    except pandas_datareader._utils.RemoteDataError:
        print(f"Stock ticker {ticker} does not exist or is not in yahoo finance database")
        quit()


def displayGraph(df):
    # try to graph
    wantToSee = input("Do you want to see the graph?(y or n): ")
    if wantToSee == 'y':
        plt.style.use('dark_background')
        df[0]["Adj Close"].plot()
        plt.title(f"Stock Prices of {df[1]}")
        plt.ylabel("Price ($)")
        plt.show()
    else:
        print("exiting program...")


data = gatherData()
displayGraph(data)
