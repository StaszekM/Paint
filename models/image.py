from tkinter import *
from models.paintingOptions import PaintingOptions
import math


class Image(Canvas):
    def __init__(self, painting_options: PaintingOptions, *args, **kw):
        self.canvas = super().__init__(*args, background='#FFFFFF', width=800, height=600, **kw)
        self.last_mouse_x = None
        self.last_mouse_y = None
        self.painting_options = painting_options

        self.eraser_cursor = self.create_oval(10, 10, 5, 5, outline='#000000', fill='#FFFFFF', state='hidden',
                                              tags=('ui',))

    def begin_drawing(self, event):
        self.last_mouse_x, self.last_mouse_y = event.x, event.y

    def draw_line_to(self, x, y):
        if self.painting_options.eraser_enabled:
            self.create_line(self.last_mouse_x, self.last_mouse_y, x, y, fill=self.painting_options.eraser_color,
                             width=self.painting_options.eraser_width, tags=('drawing',), state='disabled')
            self.tag_raise('ui', 'all')
            self.move_mouse(x, y)

        else:
            self.create_line(self.last_mouse_x, self.last_mouse_y, x, y, fill=self.painting_options.brush_color,
                             width=self.painting_options.brush_width, tags=('drawing',), state='disabled')

        self.last_mouse_x, self.last_mouse_y = x, y

    def toggle_eraser(self, active):
        if active:
            self.config(cursor="none")
            self.itemconfigure(self.eraser_cursor, state='normal')
        else:
            self.config(cursor="arrow")
            self.itemconfigure(self.eraser_cursor, state='hidden')

    def move_mouse(self, x, y):
        half_width = math.floor(self.painting_options.eraser_width / 2)
        self.coords(self.eraser_cursor, x - half_width, y - half_width, x + half_width, y + half_width)

    def pick_color(self, x, y):
        ids = self.find_overlapping(x, y, x, y)

        if len(ids) > 0:
            index = ids[-1]
            color = self.itemcget(index, "fill")
            color = color.upper()
            return color

        return "#FFFFFF"
