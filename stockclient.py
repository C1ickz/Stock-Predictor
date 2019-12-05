import socket
import time


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

    # validates stock ticker input
    def validate(self, tkr):
        self.s.sendall(tkr.encode('UTF-8'))
        return self.check_validation()

    def check_validation(self):
        inp = self.s.recv(1024).decode('UTF-8')
        return inp

    # requests data from server
    def send_request(self, request):
        self.s.sendall(request.encode('UTF-8'))

    # receives prediction
    def rec_pred(self):
        pred = self.s.recv(1024).decode('UTF-8')
        return pred

    # receives data from server
    def receive(self):
        self.s.setblocking(1)
        data = []
        inp = ''
        begin = time.time()
        print('before while')
        while True:
            if time.time() - begin > 3:
                break
            print('in while')
            try:
                inp = self.s.recv(4096)
                if not inp: break
                if inp:
                    data.append(inp)

                    begin = time.time()
                else:
                    time.sleep(0.1)

            except Exception as e:
                print(str(e))
                break
                pass
        print('while has finished')
        rec = b''.join(data)
        with open('imgFile.png', 'wb') as f:
            f.write(rec)

    def close(self):
        self.s.close()
