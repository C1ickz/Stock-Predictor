from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class TestApp(App):
    def build(self):
        self.title = "Stock Price Predictor"
        return HomeScreen()


class HomeScreen(GridLayout):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="Input a Stock Ticker"))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text="Predicted Stock Price ${}".format("INSERT PRICE HERE")))


TestApp().run()
