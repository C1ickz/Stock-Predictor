import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime as dt

start = dt.datetime(2018, 1, 3)  # (YEAR, MONTH, DAY)
end = dt.datetime(2019, 10, 9)

ticker = input("input ticker (NOTE: This is not being error checked): ").upper()
# f = web.DataReader(ticker, 'stooq', start, end) # if ticker does not work add ^ in front aka ^tkr
f = web.DataReader(ticker, 'yahoo', start, end)  # if ticker does not work add ^ in front aka ^tkr

print(f.tail(10))  # prints first 10 lines of stock data
print("-----------")
print(f['Adj Close'])

# try to graph
wantToSee = input("Do you want to see the graph?(y or n): ")
if wantToSee == 'y':
	# f["Close"].plot()
	plt.style.use('dark_background') # For more info on styles visit https://pythonprogramming.net/styles-matplotlib-tutorial/
	f["Adj Close"].plot()
	plt.title("Stock Prices of {}".format(ticker))
	plt.ylabel("Price ($)")
	plt.show()
else:
    print("exiting program...")
