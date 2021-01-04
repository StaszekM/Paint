from models import paintingOptions, image
from views.window import Window
from controllers.canvasController import CanvasController

if __name__ == '__main__':
    painting_options = paintingOptions.PaintingOptions()

    canvas_controller = CanvasController(None, painting_options)
    root = Window(None, canvas_controller)

    image = image.Image()

    image.bind("<B1-Motion>", canvas_controller.on_motion)
    image.bind("<1>", canvas_controller.on_mouse_down)

    root.image = image
    canvas_controller.image = image

    root.setup()
    root.mainloop()