from tkinter import Tk
from models.image import Image
from controllers.canvasController import CanvasController


class Window(Tk):
    def __init__(self, image: Image, controller: CanvasController, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = image
        self.controller = controller

    def setup(self):
        self.image.master = self
        self.image.pack()
