from tkinter import *
from models.paintingOptions import PaintingOptions


class Image(Canvas):
    def __init__(self, *args, **kw):
        super().__init__(*args, background='#FFFFFF', **kw)
        self.last_mouse_x = None
        self.last_mouse_y = None

    def begin_drawing(self, event):
        self.last_mouse_x, self.last_mouse_y = event.x, event.y

    def draw_line_to(self, x, y, options: PaintingOptions):
        self.create_line(self.last_mouse_x, self.last_mouse_y, x, y, fill=options.brush_color,
                         width=options.brush_width)
        self.last_mouse_x, self.last_mouse_y = x, y
