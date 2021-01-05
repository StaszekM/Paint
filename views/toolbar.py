from tkinter import *


class Toolbar(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, background='#FF0000', **kwargs)
        self.eraser_button = Button(self, text='Erase', background='#FFFFFF')

    def setup(self):
        self.eraser_button.pack()

    def toggle_eraser_active(self, active):
        self.eraser_button.configure(background='#00FF00' if active else '#FFFFFF')
