from models.image import Image
from models.paintingOptions import PaintingOptions


class CanvasController:
    def __init__(self, image: Image, options: PaintingOptions):
        self.image = image
        self.painting_options = options

    def on_motion(self, event):
        self.image.draw_line_to(event.x, event.y, self.painting_options)

    def on_mouse_down(self, event):
        self.image.last_mouse_x, self.image.last_mouse_y = event.x, event.y
