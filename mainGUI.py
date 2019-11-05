from tkinter import *
from tkinter import messagebox
# from SimpleStocksAndGraph import Stock
from stockclient import StockPSocket

window = Tk()
window.title('Stock Predictor')
window.geometry('350x200')

lbl = Label(window, text='Input Stock Ticker')
lbl.grid(column=0, row=0)
txt = Entry(window, width=10)
txt.grid(column=1, row=0)


def clicked_tkr():
    ticker = ""
    try:
        if txt.get().strip():
            ticker = txt.get().strip()
        else:
            raise ValueError('Empty string')

        client_socket = StockPSocket('192.168.0.117', 9998)
        client_socket.send_request(ticker)
        prediction = client_socket.receive()
        client_socket.close()
    except ValueError as e:
        messagebox.showinfo('Invalid', 'Please enter a proper stock ticker.')
    return prediction


btn = Button(window, text='Submit', command=clicked_tkr)
btn.grid(column=2, row=0)

window.mainloop()
