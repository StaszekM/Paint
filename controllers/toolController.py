from models.paintingOptions import PaintingOptions
from views.toolbar import Toolbar
from models.image import Image


class ToolController:
    def __init__(self, toolbar: Toolbar, image: Image, painting_options: PaintingOptions):
        self.painting_options = painting_options
        self.toolbar = toolbar
        self.image = image

    def on_toggle_eraser(self):
        self.painting_options.eraser_enabled = not self.painting_options.eraser_enabled
        self.toolbar.toggle_eraser_active(self.painting_options.eraser_enabled)
        self.image.toggle_eraser(self.painting_options.eraser_enabled)
