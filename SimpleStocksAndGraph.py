import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime as dt


def gatherData():
    start = dt.datetime(2018, 1, 3)  # (YEAR, MONTH, DAY)
    end = dt.datetime(2019, 10, 9)
    ticker = input("input ticker (NOTE: This is not being error checked): ").upper()
    df = web.DataReader(ticker, 'yahoo', start, end)  # if ticker does not work add ^ in front aka ^tkr
    # print(df.tail(10))  # prints first 10 lines of stock data
    # print("-----------")
    # print(df['Adj Close'])

    return df, ticker


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
