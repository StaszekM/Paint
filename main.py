from models.paintingOptions import PaintingOptions
from models.image import Image
from views.window import Window
from views.toolbar import Toolbar
from controllers.canvasController import CanvasController
from controllers.toolController import ToolController

if __name__ == '__main__':
    painting_options = PaintingOptions()

    tool_controller = ToolController(None, None, painting_options)
    canvas_controller = CanvasController(None, painting_options, tool_controller)

    root = Window(None, None, canvas_controller)

    toolbar = Toolbar(painting_options)
    image = Image(painting_options)

    image.bind("<B1-Motion>", canvas_controller.on_mouse_drag)
    image.bind("<1>", canvas_controller.on_mouse_down)
    image.bind("<Motion>", canvas_controller.on_mouse_move)
    image.bind("<B1-ButtonRelease>", canvas_controller.on_mouse_up)

    toolbar.eraser_button.configure(command=tool_controller.on_toggle_eraser)
    toolbar.color_picker_button.configure(command=tool_controller.on_change_color_click)
    toolbar.brush_width_button.configure(command=tool_controller.on_change_brush_width_click)
    toolbar.canvas_color_picker_button.configure(command=tool_controller.on_canvas_color_picker_click)

    root.image = image
    root.toolbar = toolbar
    canvas_controller.image = image
    tool_controller.toolbar = toolbar
    tool_controller.image = image

    toolbar.setup()
    root.setup()
    root.mainloop()
