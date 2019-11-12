# echo server
import socket
import pickle
import pandas_datareader as web
import datetime as dt

# creates server socket


serverS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ipv4 address of server
host = '192.168.0.117'

port = 9998

serverS.bind((host, port))

# queue up to 20 concurrent requests
serverS.listen(20)


def validate_tkr(tkr):
    # block gets current date and sets appropriate variables
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
    print(tkr)
    # block gets current date and sets appropriate variables
    d = dt.datetime.today()
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
    tkr_ending = tkr[len(tkr)-1:len(tkr)]
    tkr = tkr[0:len(tkr)-1]
    print(tkr, tkr_ending)

    if tkr_ending == 'p':
        pass  # this is where prediction method call will be placed
    elif tkr_ending == 'v':
        curr_conn.sendall(validate_tkr(tkr).encode('UTF-8'))
        print('inv')
    elif tkr_ending == 'r':
        curr_conn.sendall(gather_data(tkr))
    print('Send Successful')
