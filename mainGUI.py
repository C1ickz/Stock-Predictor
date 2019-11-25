# Developed by: Jordan Davis and Ryan Harris
#
# Emails: davisja2023@mountunion.edu and harrisrl2023@mountunion.edu
#
# Description:This program has a user-facing GUI that interacts
# with a server. The server predicts future stock prices using
# an Long-Short-Term-Memory (LSTM) network. The training of
# the model takes place on the server and the result of the
# prediction is sent back to the client with as little latency
# as possible.
#
# NOTE: The server object was also designed and implemented
# by Jordan Davis and Ryan Harris.

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar, Button, Label, Entry
from stockclient import StockPSocket
from PIL import Image, ImageTk


class MainGUI:
    def __init__(self, master):
        # sets host and port of server
        self.host = '192.168.216.18'
        self.port = 9998

        # sets up empty var for ticker
        self.tkr = ''

        # sets up prediction variable
        self.prediction = 0

        self.master = master
        master.title('Stock Predictor')
        master.geometry('800x600')

        # creates label
        self.lbl = Label(master, text='Input Stock Ticker')
        self.lbl.pack(side=TOP)

        # creates text field
        self.txt = Entry(master, width=10)
        self.txt.pack(side=TOP)

        # creates submission button
        self.btn = Button(master, text='Submit', command=self.clicked_tkr)
        self.btn.pack(side=TOP)

        # creates prediction output label
        self.p_out_lbl = Label(master, text=self.get_prediction())
        self.p_out_lbl.pack(side=BOTTOM)

        # creates prediction explicit label
        self.p_lbl = Label(master, text='Prediction: ')
        self.p_lbl.pack(side=BOTTOM)

    def get_graph(self):
        pass



    def disp_graph(self):
        img = Image.open('imgFile.png')
        render = ImageTk.PhotoImage(img)
        # create image label
        img = Label(self.master, image=render)
        img.image = render
        img.place(x=75, y=70)


    def clicked_tkr(self):
        ticker = ""
        try:
            if self.txt.get().strip():
                ticker = self.txt.get().strip()
            else:
                raise ValueError('Empty string')

            self.update_prediction_out('Please wait..')

            client_socket = StockPSocket(self.host, self.port)
            if client_socket.validate(ticker + 'v') == 'error':
                client_socket.close()
                raise ValueError()
            else:
                self.tkr = ticker
                client_socket = StockPSocket(self.host, self.port)
                client_socket.send_request(self.tkr + 'r')
                self.df = client_socket.receive()
                client_socket.close()
                self.disp_graph()

            self.update_prediction_out(90) # after Ryan finishes lstm prediction

        except ValueError as e:
            messagebox.showinfo('Invalid Ticker', 'Please enter a proper stock ticker.')

    def set_prediction(self, prediction):
        self.prediction = prediction

    def get_prediction(self):
        return self.prediction

    def update_prediction_out(self, prediction):
        self.set_prediction(prediction)
        self.p_out_lbl['text'] = self.get_prediction()
        self.p_out_lbl.update()


root = Tk()
my_gui = MainGUI(root)
root.mainloop()
