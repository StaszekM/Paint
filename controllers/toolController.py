from models.paintingOptions import PaintingOptions
from views.toolbar import Toolbar
from models.image import Image
import tkinter.colorchooser
import tkinter.simpledialog
import tkinter.messagebox


class ToolController:
    def __init__(self, toolbar: Toolbar, image: Image, painting_options: PaintingOptions):
        self.painting_options = painting_options
        self.toolbar = toolbar
        self.image = image

    def on_change_color_click(self):
        response = tkinter.colorchooser.askcolor(self.painting_options.brush_color)
        if response[1] is None:
            return
        self.painting_options.brush_color = response[1]
        self.toolbar.update_display()

    def on_toggle_eraser(self):
        self.painting_options.eraser_enabled = not self.painting_options.eraser_enabled
        self.image.toggle_eraser(self.painting_options.eraser_enabled)
        self.toolbar.update_display()

    def on_change_brush_width_click(self):
        response = 0
        while response < 1 or response > 10:
            response = tkinter.simpledialog.askinteger('Brush', 'Set brush width (in pixels), min 1, max 10')
            if response < 1 or response > 10:
                tkinter.messagebox.showwarning('Error', 'Brush width should be between 1px and 10px.')
        self.painting_options.brush_width = response
        self.toolbar.update_display()
