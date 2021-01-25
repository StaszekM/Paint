from enum import Enum


class SelectState(Enum):
    DISABLED = 1
    ENABLED = 2
    SELECTING = 3
    PLACING = 4


class PaintingOptions:
    def __init__(self):
        self.brush_color = '#000000'
        self.brush_width = 1

        self.eraser_enabled = False
        self.eraser_color = '#FFFFFF'
        self.eraser_width = 10

        self.canvas_color_picker_enabled = False
        self.canvas_select_state = SelectState.DISABLED
