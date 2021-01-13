from models.paintingOptions import PaintingOptions
from views.toolbar import Toolbar
from models.image import Image
import tkinter.colorchooser
import tkinter.simpledialog
import tkinter.filedialog
import tkinter.messagebox
from PIL import Image as PilImage
import io


class ToolController:
    def __init__(self, toolbar: Toolbar, image: Image, painting_options: PaintingOptions):
        self.painting_options = painting_options
        self.toolbar = toolbar
        self.image = image

    def on_change_color_click(self):
        response = tkinter.colorchooser.askcolor(self.painting_options.brush_color)
        if response[1] is None:
            return
        self.painting_options.brush_color = response[1]
        self.update()

    def on_toggle_eraser(self):
        self.painting_options.eraser_enabled = not self.painting_options.eraser_enabled
        self.image.toggle_eraser(self.painting_options.eraser_enabled)
        self.update()

    def on_change_brush_width_click(self):
        response = 0
        while response < 1 or response > 10:
            response = tkinter.simpledialog.askinteger('Brush', 'Set brush width (in pixels), min 1, max 10')
            if response is None:
                return
            if response < 1 or response > 10:
                tkinter.messagebox.showwarning('Error', 'Brush width should be between 1px and 10px.')
        self.painting_options.brush_width = response
        self.update()

    def on_canvas_color_picker_click(self):
        self.painting_options.canvas_color_picker_enabled = not self.painting_options.canvas_color_picker_enabled
        self.update()

    def on_save_as_button_click(self):
        path = tkinter.filedialog.asksaveasfile('w', filetypes=['Pictures {png}'], defaultextension='.png')
        if path is None:
            return

        width, height = self.image.winfo_width(), self.image.winfo_height()

        postscript = self.image.postscript(colormode='color', pagewidth=width, pageheight=height)
        try:
            img = PilImage.open(io.BytesIO(postscript.encode('utf-8')))
            img = img.resize((width, height))
            img.save(path.name, format='png')

            # self.image.delete('drawing')
            # self.imageloaded = ImageTk.PhotoImage(PilImage.open(path.name))
            # self.image.create_image(0, 0, anchor=NW, image=self.imageloaded, tags=('drawing',))

        except OSError:
            tkinter.messagebox.showerror('Error', 'Could not save file. Make sure you have Ghostscript installed.')

    def update(self):
        self.toolbar.update_display()
