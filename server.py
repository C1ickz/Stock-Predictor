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
def test(name):
    return 'Jordan\'s laptop says, Hello {}!'.format(name)


# print at starts
print('Waiting for connections...')

while True:
    curr_conn, addr = serverS.accept()
    print('Log: connection made by: {}'.format(addr))
    data = curr_conn.recv(2048).decode('UTF-8')
    data = data.split(',')
    data = [x.strip() for x in data]
    try:
        if data != data: raise ValueError()
        if data[0] == 'submit':
            curr_conn.sendall(test(data[1]).encode('UTF-8'))
        else:
            raise TypeError()
    except (IndexError, TypeError, ValueError):
        curr_conn.sendall('error occured in submission'.encode('UTF-8'))
