from tkinter import Tk
from views.toolbar import Toolbar
from models.image import Image
from controllers.canvasController import CanvasController


class Window(Tk):
    def __init__(self, image: Image, toolbar: Toolbar, controller: CanvasController, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = image
        self.controller = controller
        self.toolbar = toolbar

    def __create_grid(self):
        self.rowconfigure(0, minsize=50, weight=0)
        self.rowconfigure(1, minsize=100, weight=1)
        self.columnconfigure(0, weight=1)

    def setup(self):
        self.__create_grid()
        self.image.master = self
        self.toolbar.master = self
        self.toolbar.grid(row=0, column=0, sticky='NESW')
        self.image.grid(row=1, column=0, sticky='NW')
