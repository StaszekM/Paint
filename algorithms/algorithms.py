from abc import ABC, abstractmethod
from PIL import Image as PilImage
from PIL import ImageFilter, ImageOps

import random


class Processor(ABC):
    @abstractmethod
    def process(self, image: PilImage) -> PilImage:
        pass


class GaussianBlur(Processor):
    def process(self, image: PilImage) -> PilImage:
        return image.filter(ImageFilter.BLUR)


class ColorInverter(Processor):
    def process(self, image: PilImage) -> PilImage:
        return ImageOps.invert(image)


class Colorizer(Processor):
    def process(self, image: PilImage) -> PilImage:
        white_color = '#%02x%02x%02x' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        black_color = '#%02x%02x%02x' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return ImageOps.colorize(image.convert("L"), black=black_color, white=white_color)
