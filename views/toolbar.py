from tkinter import *
from models.paintingOptions import PaintingOptions


class Toolbar(Frame):
    def __init__(self, painting_options: PaintingOptions, *args, **kwargs):
        super().__init__(*args, background='#FF0000', **kwargs)
        self.painting_options = painting_options

        self.eraser_button = Button(self, text='Erase', background='#FFFFFF')
        self.color_picker_button = Button(self, bg=painting_options.brush_color)
        self.brush_width_button = Button(self, text=painting_options.brush_width)
        self.canvas_color_picker_button = Button(self, text='Pick from canvas')
        self.save_as_button = Button(self, text='Save')

    def setup(self):
        self.eraser_button.grid(row=0, column=0)
        self.color_picker_button.grid(row=0, column=1)
        self.brush_width_button.grid(row=0, column=2)
        self.canvas_color_picker_button.grid(row=0, column=3)
        self.save_as_button.grid(row=0, column=4)

    def update_display(self):
        self.eraser_button.configure(bg='#00FF00' if self.painting_options.eraser_enabled else '#FFFFFF')
        self.color_picker_button.configure(bg=self.painting_options.brush_color)
        self.brush_width_button.configure(text=self.painting_options.brush_width)
        self.canvas_color_picker_button.configure(
            bg='#00FF00' if self.painting_options.canvas_color_picker_enabled else '#FFFFFF')
        self.eraser_button.configure(
            state='disabled' if self.painting_options.canvas_color_picker_enabled else 'normal')
        self.canvas_color_picker_button.configure(
            state='disabled' if self.painting_options.eraser_enabled else 'normal')
