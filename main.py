from models import paintingOptions, image
from views.window import Window
from views.toolbar import Toolbar
from controllers.canvasController import CanvasController
from controllers.toolController import ToolController

if __name__ == '__main__':
    painting_options = paintingOptions.PaintingOptions()

    canvas_controller = CanvasController(None, painting_options)
    tool_controller = ToolController()

    root = Window(None, None, canvas_controller)

    toolbar = Toolbar(tool_controller)
    image = image.Image()

    image.bind("<B1-Motion>", canvas_controller.on_mouse_drag)
    image.bind("<1>", canvas_controller.on_mouse_down)

    root.image = image
    root.toolbar = toolbar
    canvas_controller.image = image

    root.setup()
    root.mainloop()
