# echo server
import socket
import pandas as pd
import pickle
import pandas_datareader as web
import datetime as dt
import datetime

# creates server socket
serverS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ipv4 address of server
host = '192.168.0.107'

port = 9998

serverS.bind((host, port))

# queue up to 20 concurrent requests
serverS.listen(20)


# retrieves data from online server
def gather_data(tkr):
    # block gets current date and sets appropriate variables
    d = datetime.datetime.today()
    year = d.year
    month = d.month
    day = d.day

    start = dt.datetime(2010, 1, 3)  # (YEAR, MONTH, DAY)
    end = dt.datetime(year, month, day)
    df = web.DataReader(tkr, 'yahoo', start, end)
    df = pickle.dumps(df)
    return df


# print at start
print('Waiting for connection...')

while True:
    curr_conn, addr = serverS.accept()
    print(f'Log: connection made by: {addr}')
    tkr = curr_conn.recv(2048).decode('UTF-8')

    try:
        curr_conn.send(gather_data(tkr))
        print('Send Successful')
    except Exception:
        print('Error occurred in sending')