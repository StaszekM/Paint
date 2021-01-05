from models import paintingOptions, image
from views.window import Window
from views.toolbar import Toolbar
from controllers.canvasController import CanvasController
from controllers.toolController import ToolController

if __name__ == '__main__':
    painting_options = paintingOptions.PaintingOptions()

    canvas_controller = CanvasController(None, painting_options)
    tool_controller = ToolController(None, None, painting_options)

    root = Window(None, None, canvas_controller)

    toolbar = Toolbar()
    image = image.Image(painting_options)

    image.bind("<B1-Motion>", canvas_controller.on_mouse_drag)
    image.bind("<1>", canvas_controller.on_mouse_down)
    image.bind("<Motion>", canvas_controller.on_mouse_move)

    toolbar.eraser_button.configure(command=tool_controller.on_toggle_eraser)

    root.image = image
    root.toolbar = toolbar
    canvas_controller.image = image
    tool_controller.toolbar = toolbar
    tool_controller.image = image

    toolbar.setup()
    root.setup()
    root.mainloop()
