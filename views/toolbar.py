from tkinter import *
from models.paintingOptions import PaintingOptions


class Toolbar(Frame):
    def __init__(self, painting_options: PaintingOptions, *args, **kwargs):
        super().__init__(*args, background='#FF0000', **kwargs)
        self.painting_options = painting_options
        self.eraser_button = Button(self, text='Erase', background='#FFFFFF')
        self.color_picker_button = Button(self, bg='#000000')

    def setup(self):
        self.eraser_button.pack()
        self.color_picker_button.pack()

    def update_display(self):
        self.eraser_button.configure(background='#00FF00' if self.painting_options.eraser_enabled else '#FFFFFF')
        self.color_picker_button.configure(bg=self.painting_options.brush_color)
