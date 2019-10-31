import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime as dt
from glob import glob
import datetime


def gatherData():

    #block gets current date and sets appropriate variables
    d = dt.datetime.today()
    year = d.year
    month = d.month
    day = d.day

    start = dt.datetime(2010, 1, 3)  # (YEAR, MONTH, DAY)
    end = dt.datetime(year, month, day)

    response = input('Would you like write data to a new file(y or n)? ').upper()
    if not response.find("Y"):
        file = input("Please input file name you want the data written to: ")

        if '.csv' not in file:
            file = file + '.csv'

    elif not response.find('N'):
        print(glob('*.csv'))
        index = int(input('Please enter a integer representing index of the csv file you wish to use: '))
        file = glob('*.csv')[index]

    try:
        ticker = input("input ticker: ").upper()
        df = web.DataReader(ticker, 'yahoo', start, end)
        df.to_csv(file)

        return df, ticker

    except web._utils.RemoteDataError:
        print(f"Stock ticker {ticker} does not exist, or is not in yahoo finance database")
        quit()


def displayGraph(df):
    # try to graph
    ticker = df[1]
    wantToSee = input("Do you want to see the graph?(y or n): ")
    if wantToSee == 'y':
        fig = plt.figure(f"Graph of {ticker}'s Stock History")
        plt.style.use('ggplot')
        df[0]["Adj Close"].plot()
        plt.title(f"Stock Prices of {ticker}")
        plt.ylabel("Price ($)")
        plt.show()
    else:
        print("exiting program...")


data = gatherData()
displayGraph(data)
