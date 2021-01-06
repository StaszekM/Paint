from models.paintingOptions import PaintingOptions
from views.toolbar import Toolbar
from models.image import Image
import tkinter.colorchooser

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
        self.toolbar.color_picker_button.configure(bg=response[1])

    def on_toggle_eraser(self):
        self.painting_options.eraser_enabled = not self.painting_options.eraser_enabled
        self.toolbar.toggle_eraser_active(self.painting_options.eraser_enabled)
        self.image.toggle_eraser(self.painting_options.eraser_enabled)
