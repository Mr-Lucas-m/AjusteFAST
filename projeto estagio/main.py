import webview
from tkinter import Tk
from controller.controle import Controller
api = Controller()
window = webview.create_window('ajuste', './view/main.html', width=600, height=430, js_api=api, resizable=False)
webview.start(debug=False)
