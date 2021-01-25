from models.image import Image
from models.paintingOptions import PaintingOptions, SelectState
from controllers.toolController import ToolController


class CanvasController:
    def __init__(self, image: Image, options: PaintingOptions, tool_controller: ToolController):
        self.image = image
        self.painting_options = options
        self.tool_controller = tool_controller

    def on_mouse_drag(self, event):
        if self.painting_options.eraser_enabled:
            self.image.erase_to(event.x, event.y)
        elif self.painting_options.canvas_select_state in [SelectState.ENABLED, SelectState.SELECTING]:
            if self.painting_options.canvas_select_state == SelectState.ENABLED:
                self.painting_options.canvas_select_state = SelectState.SELECTING
                self.tool_controller.update()
            self.image.draw_select_to(event.x, event.y)
        else:
            self.image.draw_line_to(event.x, event.y)
        self.tool_controller.update()

    def on_mouse_down(self, event):
        if not self.painting_options.canvas_color_picker_enabled:
            self.image.begin_drawing(event)
        if self.painting_options.canvas_select_state == SelectState.PLACING:
            self.image.draw_selected_fragment_at(event.x, event.y)
            self.painting_options.canvas_select_state = SelectState.DISABLED
        self.tool_controller.update()

    def on_mouse_move(self, event):
        self.image.move_mouse(event.x, event.y)
        if self.painting_options.canvas_select_state == SelectState.PLACING:
            self.image.move_selected_fragment_to(event.x, event.y)
        self.tool_controller.update()

    def on_mouse_up(self, event):
        if self.painting_options.canvas_color_picker_enabled:
            color = self.image.pick_color(event.x, event.y)
            self.painting_options.brush_color = color
            self.painting_options.canvas_color_picker_enabled = False
            self.tool_controller.update()
        if self.painting_options.canvas_select_state in [SelectState.SELECTING, SelectState.ENABLED]:
            if self.painting_options.canvas_select_state == SelectState.SELECTING:
                self.image.pick_selection()
                self.painting_options.canvas_select_state = SelectState.PLACING
            else:
                self.image.toggle_selector_rectangle(False)
                self.painting_options.canvas_select_state = SelectState.DISABLED
        self.tool_controller.update()
