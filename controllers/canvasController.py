from models.image import Image
from models.paintingOptions import PaintingOptions
from controllers.toolController import ToolController


class CanvasController:
    def __init__(self, image: Image, options: PaintingOptions, tool_controller: ToolController):
        self.image = image
        self.painting_options = options
        self.tool_controller = tool_controller

    def on_mouse_drag(self, event):
        if not self.painting_options.canvas_color_picker_enabled:
            self.image.draw_line_to(event.x, event.y)

    def on_mouse_down(self, event):
        if not self.painting_options.canvas_color_picker_enabled:
            self.image.begin_drawing(event)

    def on_mouse_move(self, event):
        self.image.move_mouse(event.x, event.y)

    def on_mouse_up(self, event):
        if self.painting_options.canvas_color_picker_enabled:
            color = self.image.pick_color(event.x, event.y)
            self.painting_options.brush_color = color
            self.painting_options.canvas_color_picker_enabled = False
            self.tool_controller.update()
