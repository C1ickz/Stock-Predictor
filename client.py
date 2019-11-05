import socket

#creates socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#gets local machine name
host = '192.168.0.105'

port = 9998

#makes connection
s.connect((host, port))

prompt = 'Input submit, name (ie. submit, Joe): '
s.send(input(prompt).encode('UTF-8'))

#sets recieving limit to 1024 bytes
msg = s.recv(1024)

s.close()
print(msg.decode('UTF-8'))