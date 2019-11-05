# echo server

import socket

serverS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ipv4 address of server
host = '192.168.0.117'

port = 9998

serverS.bind((host, port))

# queue up to 20 concurrent requests
serverS.listen(20)


# test method
def test(tkr, pred=90):
    return '{} has a predicted value of ${}'.format(tkr, pred)


# print at starts
print('Waiting for connections...')

while True:
    curr_conn, addr = serverS.accept()
    print('Log: connection made by: {}'.format(addr))
    tkr = curr_conn.recv(2048).decode('UTF-8')
    try:
        curr_conn.sendall(test(tkr).encode('UTF-8'))

    except Exception as e:
        print(e.with_traceback())
        curr_conn.sendall('Error occurred in submission'.encode('UTF-8'))
