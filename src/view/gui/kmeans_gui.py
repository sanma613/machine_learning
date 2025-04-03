from kivy.app import App


from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

import sys
sys.path.append("src")

from model.KmeansLogic import Kmeans

class KmeansApp(App):
    def build(self):
        canvas = GridLayout(rows=7)

        canvas.add_widget(Label(text="Ingresa la ruta del dataset:"))
        self.file_path = TextInput()
        canvas.add_widget(self.file_path)

        canvas.add_widget(Label(text="Ingresa el numero de centrodes:"))
        self.centroids = TextInput(input_filter="int")
        canvas.add_widget(self.centroids)

        canvas.add_widget(Label(text="Ingresa las iteraciones que deseas realizar:"))
        self.iterations = TextInput(input_filter="int")
        canvas.add_widget(self.iterations)
        
        submit_button = Button(text="Mostrar Gráficos")

        return canvas

KmeansApp().run()