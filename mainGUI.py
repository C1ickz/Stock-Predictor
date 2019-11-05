from tkinter import *
from tkinter import messagebox
from stockclient import StockPSocket


class MainGUI:
    def __init__(self, master):

        # sets up prediction variable
        self.prediction = 0

        self.master = master
        master.title('Stock Predictor')
        master.geometry('400x300')

        # creates label
        self.lbl = Label(master, text='Input Stock Ticker')
        self.lbl.grid(column=0, row=0)

        # creates text field
        self.txt = Entry(master, width=10)
        self.txt.grid(column=1, row=0)

        # creates submission button
        self.btn = Button(master, text='Submit', command=self.clicked_tkr)
        self.btn.grid(column=2, row=0)

        # creates prediction explicit label
        self.p_lbl = Label(master, text='Prediction: ')
        self.p_lbl.grid(column=0, row=2)

        self.p_out_lbl = Label(master, text=self.get_prediction())
        self.p_out_lbl.grid(column=1, row=2)

    def clicked_tkr(self):
        ticker = ""
        try:
            if self.txt.get().strip():
                ticker = self.txt.get().strip()
            else:
                raise ValueError('Empty string')

            client_socket = StockPSocket('192.168.0.117', 9998)
            client_socket.send_request(ticker)
            self.update_prediction_out(client_socket.receive())
            client_socket.close()

        except ValueError as e:
            messagebox.showinfo('Invalid', 'Please enter a proper stock ticker.')

    def set_prediction(self, prediction):
        self.prediction = prediction

    def get_prediction(self):
        return self.prediction

    def update_prediction_out(self, prediction):
        self.set_prediction(prediction)
        self.p_out_lbl['text'] = self.get_prediction()



root = Tk()
my_gui = MainGUI(root)
root.mainloop()
