import socket


class StockPSocket:
    def __init__(self, host, port):
        # creates socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # IPv4 address of server
        self.host = host
        # port of server
        self.port = port
        # makes connection
        try:
            print(self.host, self.port)
            self.s.connect((self.host, self.port))
        except OSError:
            print('Error occurred when connecting to server')
            raise ConnectionRefusedError()

    def send_request(self, request):
        self.s.sendall(request.encode('UTF-8'))

    def receive(self):
        return self.s.recv(1024).decode('UTF-8')

    def close(self):
        self.s.close()
