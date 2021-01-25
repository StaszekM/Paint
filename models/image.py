from tkinter import *
from PIL import Image as PilImage
from PIL import ImageTk
from models.paintingOptions import PaintingOptions, SelectState
from algorithms.algorithms import Processor
import math
import io


class Image(Canvas):
    def __init__(self, painting_options: PaintingOptions, *args, **kw):
        self.canvas = super().__init__(*args, background='#FFFFFF', width=800, height=600, **kw)
        self.image_temp = None
        self.last_mouse_x = None
        self.last_mouse_y = None
        self.select_top_left_x = None
        self.select_top_left_y = None
        self.painting_options = painting_options

        self.eraser_cursor = self.create_oval(10, 10, 5, 5, outline='#000000', fill='#FFFFFF', state='hidden',
                                              tags=('ui',))
        self.selector_rectangle = self.create_rectangle(10, 10, 50, 50, outline='#000000', fill=None, state='hidden',
                                                        tags=('ui',))
        self.selected_fragment = None
        self.selected_fragment_temp = None

        self.drawn_images = []

    def begin_drawing(self, event):
        self.last_mouse_x, self.last_mouse_y = event.x, event.y
        self.tag_raise('ui', 'all')
        if self.painting_options.canvas_select_state == SelectState.ENABLED:
            self.select_top_left_x, self.select_top_left_y = event.x, event.y
            self.coords(self.selector_rectangle, event.x, event.y, event.x, event.y)
            self.toggle_selector_rectangle(True)

    def draw_line_to(self, x, y):
        self.create_line(self.last_mouse_x, self.last_mouse_y, x, y, fill=self.painting_options.brush_color,
                         width=self.painting_options.brush_width, tags=('drawing',), state='disabled')

        self.last_mouse_x, self.last_mouse_y = x, y

    def draw_select_to(self, x, y):
        self.coords(self.selector_rectangle, self.select_top_left_x, self.select_top_left_y, x, y)
        self.tag_raise('ui', 'all')
        self.last_mouse_x, self.last_mouse_y = x, y

    def erase_to(self, x, y):
        self.create_line(self.last_mouse_x, self.last_mouse_y, x, y, fill=self.painting_options.eraser_color,
                         width=self.painting_options.eraser_width, tags=('drawing',), state='disabled')
        self.tag_raise('ui', 'all')
        self.move_mouse(x, y)
        self.last_mouse_x, self.last_mouse_y = x, y

    def pick_selection(self):
        top_left_x = max(min(self.select_top_left_x, self.last_mouse_x), 0)
        top_left_y = max(min(self.select_top_left_y, self.last_mouse_y), 0)

        bottom_right_x = max(max(self.select_top_left_x, self.last_mouse_x), 0)
        bottom_right_y = max(max(self.select_top_left_y, self.last_mouse_y), 0)

        self.toggle_selector_rectangle(False)
        img = self.get_image()
        img = img.crop((top_left_x, top_left_y, bottom_right_x, bottom_right_y))
        img = img.convert("RGBA")

        pixdata = img.load()
        width, height = img.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (255, 255, 255, 255):
                    pixdata[x, y] = (255, 255, 255, 0)

        self.selected_fragment_temp = ImageTk.PhotoImage(img)
        img.save('temp.png')
        self.selected_fragment = self.create_image(self.last_mouse_x, self.last_mouse_y, anchor=NW, tags=('ui',),
                                                   image=self.selected_fragment_temp)

    def toggle_eraser(self, active):
        if active:
            self.config(cursor="none")
            self.itemconfigure(self.eraser_cursor, state='normal')
        else:
            self.config(cursor="arrow")
            self.itemconfigure(self.eraser_cursor, state='hidden')

    def toggle_selector_rectangle(self, active):
        self.itemconfigure(self.selector_rectangle, state='normal' if active else 'hidden')

    def move_mouse(self, x, y):
        half_width = math.floor(self.painting_options.eraser_width / 2)
        self.coords(self.eraser_cursor, x - half_width, y - half_width, x + half_width, y + half_width)

    def move_selected_fragment_to(self, x, y):
        self.coords(self.selected_fragment, x, y)

    def draw_selected_fragment_at(self, x, y):
        self.drawn_images.append(PhotoImage(file='temp.png'))
        self.delete(self.selected_fragment)
        self.create_image(x, y, anchor=NW, tags=('drawing',),
                          image=self.drawn_images[len(self.drawn_images) - 1])

    def abort_placing(self):
        self.delete(self.selected_fragment)

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

    def draw_image(self, path):
        self.update()
        self.delete('drawing')
        self.update()

        image = PilImage.open(path, mode='r', formats=None)
        imgWidth, imgHeight = image.size
        canvWidth, canvHeight = self.winfo_reqwidth(), self.winfo_reqheight()

        if imgWidth > canvWidth or imgHeight > canvHeight:
            imgRatio = imgWidth / imgHeight
            canvRatio = canvWidth / canvHeight
            if imgRatio > canvRatio:
                scale = imgWidth / canvWidth
            else:
                scale = imgHeight / canvHeight
            image = image.resize((int(imgWidth // scale), int(imgHeight // scale)))

        imgWidth, imgHeight = image.size

        self.image_temp = ImageTk.PhotoImage(image)
        self.create_image((canvWidth - imgWidth) / 2, (canvHeight - imgHeight) / 2, anchor=NW, image=self.image_temp,
                          tags=('drawing',))
