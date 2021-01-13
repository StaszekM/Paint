from tkinter import *
from models.paintingOptions import PaintingOptions
from icons import icons
import colorsys


class Toolbar(Frame):
    def __init__(self, painting_options: PaintingOptions, *args, **kwargs):
        super().__init__(*args, background='#B5F5FF', **kwargs)
        self.painting_options = painting_options
        self.images = [PhotoImage(file=icon) for icon in
                       [icons.eraser, icons.paint, icons.width, icons.colorpicker, icons.save, icons.effect,
                        icons.paint_white]]

        self.eraser_button = Button(self, background='#FFFFFF', text='Erase', image=self.images[0], compound=BOTTOM)
        self.color_picker_button = Button(self, bg=painting_options.brush_color, text='Color', image=self.images[6],
                                          compound=BOTTOM, fg='#FFFFFF')
        self.brush_width_button = Button(self, background='#FFFFFF',
                                         text="Width: {}".format(painting_options.brush_width),
                                         image=self.images[2], compound=BOTTOM)

        self.canvas_color_picker_button = Button(self, background='#FFFFFF', text='Pick from canvas',
                                                 image=self.images[3], compound=BOTTOM)
        self.save_as_button = Button(self, background='#FFFFFF', text='Save', image=self.images[4], compound=BOTTOM)

        self.blur_button = Button(self, background='#FFFFFF', text='Blur', image=self.images[5], compound=BOTTOM)
        self.color_invert_button = Button(self, background='#FFFFFF', text='Invert colors', image=self.images[5],
                                          compound=BOTTOM)
        self.colorize_button = Button(self, background='#FFFFFF', text='Colorize', image=self.images[5],
                                      compound=BOTTOM)

    def setup(self):
        self.eraser_button.grid(row=0, column=0)
        self.color_picker_button.grid(row=0, column=1)
        self.brush_width_button.grid(row=0, column=2)
        self.canvas_color_picker_button.grid(row=0, column=3)
        self.save_as_button.grid(row=0, column=4)
        self.blur_button.grid(row=0, column=5)
        self.color_invert_button.grid(row=0, column=6)
        self.colorize_button.grid(row=0, column=7)

    def update_display(self):
        self.eraser_button.configure(bg='#00FF00' if self.painting_options.eraser_enabled else '#FFFFFF')

        color = self.painting_options.brush_color[1:]
        colorRGB = tuple([int(color[i:i + 2], 16) for i in range(0, len(color), 2)])
        _, _, v = colorsys.rgb_to_hsv(colorRGB[0] / 255, colorRGB[1] / 255, colorRGB[2] / 255)
        self.color_picker_button.configure(bg=self.painting_options.brush_color, fg='#FFFFFF' if v < 0.6 else '#000000',
                                           image=self.images[6] if v < 0.6 else self.images[1])
        self.brush_width_button.configure(text="Width: {}".format(self.painting_options.brush_width))
        self.canvas_color_picker_button.configure(
            bg='#00FF00' if self.painting_options.canvas_color_picker_enabled else '#FFFFFF')
        self.eraser_button.configure(
            state='disabled' if self.painting_options.canvas_color_picker_enabled else 'normal')
        self.canvas_color_picker_button.configure(
            state='disabled' if self.painting_options.eraser_enabled else 'normal')
