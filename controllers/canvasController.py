from models.image import Image
from models.paintingOptions import PaintingOptions


class CanvasController:
    def __init__(self, image: Image, options: PaintingOptions):
        self.image = image
        self.painting_options = options

    def on_mouse_drag(self, event):
        self.image.draw_line_to(event.x, event.y, self.painting_options)

    def on_mouse_down(self, event):
        self.image.begin_drawing(event)
