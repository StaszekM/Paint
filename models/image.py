from tkinter import *
from PIL import Image as PilImage
from PIL import ImageTk
from models.paintingOptions import PaintingOptions
from algorithms.algorithms import Processor
import math
import io


class Image(Canvas):
    def __init__(self, painting_options: PaintingOptions, *args, **kw):
        self.canvas = super().__init__(*args, background='#FFFFFF', width=800, height=600, **kw)
        self.image_temp = None
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
        img = self.get_image()
        value = img.getpixel((x, y))
        return '#%02x%02x%02x' % value

    def get_postscript(self):
        if self.painting_options.eraser_enabled:
            self.toggle_eraser(False)

        self.update()
        width, height = self.winfo_reqwidth(), self.winfo_reqheight()
        ps = self.postscript(colormode='color', pagewidth=width, pageheight=height)
        if self.painting_options.eraser_enabled:
            self.toggle_eraser(True)

        return ps

    def get_image(self):
        img = PilImage.open(io.BytesIO(self.get_postscript().encode('utf-8')))
        self.update()
        width, height = self.winfo_reqwidth(), self.winfo_reqheight()
        img.resize((width, height))
        return img

    def process_image(self, processor: Processor):
        processed_image = processor.process(self.get_image())

        self.image_temp = ImageTk.PhotoImage(processed_image)
        self.update()
        self.delete('drawing')
        self.update()
        self.create_image(0, -1, anchor=NW, image=self.image_temp, tags=('drawing',))
