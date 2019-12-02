# echo server
import socket
import pandas_datareader as web
import datetime as dt
import matplotlib.pyplot as plt
import os

# creates server socket
serverS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ipv4 address of server
host = '10.18.207.18'

port = 9998

serverS.bind((host, port))

# queue up to 20 concurrent requests
serverS.listen(20)

# creates empty dataframe
df = None


def validate_tkr(tkr):
    global df
    # gets current date and sets appropriate variables
    end_d = dt.datetime.today()
    year = end_d.year
    month = end_d.month
    day = end_d.day
    end_d = dt.datetime(year, month, day)

    one_week_ago = dt.datetime.today() - dt.timedelta(days=7)
    year = one_week_ago.year
    month = one_week_ago.month
    day = one_week_ago.day
    one_week_ago = dt.datetime(year, month, day)
    try:
        df = web.DataReader(tkr, 'yahoo', one_week_ago, end_d)
        return 'success'
    except Exception:
        return 'error'


# retrieves data from online server
def gather_data(tkr):
    global df
    print(tkr)
    # block gets current date and sets appropriate variables
    d = dt.datetime.today()
    year = d.year
    month = d.month
    day = d.day

    start = dt.datetime(2010, 1, 3)  # (YEAR, MONTH, DAY)
    end = dt.datetime(year, month, day)
    df = web.DataReader(tkr, 'yahoo', start, end)
    df = df.drop(['High', 'Low', 'Open', 'Close', 'Volume', ], axis=1)
    return df  # this is only a df containing the dates and adj close value


# makes graph and returns file
def make_g(tkr):
    global df
    df = gather_data(tkr)
    df.plot(kind='line')
    plt.title(f'Stock Price of {tkr.upper()}')
    plt.savefig('StockGraphForDisp.png')
    with open('StockGraphForDisp.png', 'rb') as f:
        by = f.read()
    os.remove('StockGraphForDisp.png')
    return by


def make_p(tkr):
    global df
    # add prediction code here
    prediction = 1
    return f'${prediction}'


# print at start
print('Waiting for connection...')

while True:
    curr_conn, addr = serverS.accept()
    print(f'Log: connection made by: {addr}')
    tkr = curr_conn.recv(2048).decode('UTF-8')
    tkr_ending = tkr[len(tkr) - 1:len(tkr)]
    tkr = tkr[0:len(tkr) - 1]
    print(tkr, tkr_ending)
    if tkr_ending == 'v':
        curr_conn.sendall(validate_tkr(tkr).encode('UTF-8'))
    elif tkr_ending == 'g':
        curr_conn.sendall(make_g(tkr))
    elif tkr_ending == 'p':
        curr_conn.sendall(make_p(tkr).encode('UTF-8'))
    print('Send Successful')
    print('***END TRANSMISSION***\n')
