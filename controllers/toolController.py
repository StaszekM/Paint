from models.paintingOptions import PaintingOptions, SelectState
from views.toolbar import Toolbar
from models.image import Image
import tkinter.colorchooser
import tkinter.simpledialog
import tkinter.filedialog
import tkinter.messagebox
from algorithms.algorithms import GaussianBlur, ColorInverter, Colorizer


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
        self.save_image(path.name)

    def on_blur_button_click(self):
        self.image.process_image(GaussianBlur())

    def on_invert_colors_button_click(self):
        self.image.process_image(ColorInverter())

    def on_posterize_button_click(self):
        self.image.process_image(Colorizer())

    def on_open_image(self):
        path = tkinter.filedialog.askopenfile('r', filetypes=['Pictures {png}', 'Pictures {jpg}'])

        if path is None:
            return

        yes_no = tkinter.messagebox.askokcancel('Opening',
                                                'Do you want to open this file? All canvas contents will be erased.')
        if not yes_no:
            return

        self.open_image(path.name)

    def on_select_button_click(self):
        if self.painting_options.canvas_select_state == SelectState.ENABLED:
            self.painting_options.canvas_select_state = SelectState.DISABLED
        elif self.painting_options.canvas_select_state == SelectState.DISABLED:
            self.painting_options.canvas_select_state = SelectState.ENABLED
        elif self.painting_options.canvas_select_state == SelectState.PLACING:
            self.image.abort_placing()
            self.painting_options.canvas_select_state = SelectState.DISABLED
        self.update()

    def update(self):
        self.toolbar.update_display()

    def save_image(self, path):
        img = self.image.get_image()
        try:
            img = img.resize((self.image.winfo_width(), self.image.winfo_height()))
            img.save(path, format='png')
        except OSError:
            tkinter.messagebox.showerror('Error', 'Could not save file. Make sure you have Ghostscript installed.')

    def open_image(self, path):
        self.image.draw_image(path)
