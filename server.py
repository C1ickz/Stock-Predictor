# echo server
import socket
import pandas as pd
import pickle

serverS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ipv4 address of server
host = '192.168.0.107'

port = 9998

serverS.bind((host, port))

# queue up to 20 concurrent requests
serverS.listen(20)


# test method
def test():
    raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
                'last_name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze'],
                'age': [42, 52, 36, 24, 73],
                'preTestScore': [4, 24, 31, 2, 3],
                'postTestScore': [25, 94, 57, 62, 70]}
    df = pd.DataFrame(raw_data, columns=['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
    to_send = pickle.dumps(df)
    return to_send


# print at starts
print('Waiting for connections...')

while True:
    curr_conn, addr = serverS.accept()
    print(f'Log: connection made by: {addr}')
    tkr = curr_conn.recv(2048).decode('UTF-8')
    try:
        curr_conn.sendall(test())

    except Exception as e:
        print(e.with_traceback())
        curr_conn.sendall('Error occurred in submission'.encode('UTF-8'))