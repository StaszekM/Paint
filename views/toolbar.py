from tkinter import *
from controllers.toolController import *


class Toolbar(Frame):
    def __init__(self, controller: ToolController, *args, **kwargs):
        super().__init__(*args, background='#FF0000', **kwargs)
        self.controller = controller
