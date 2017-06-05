"""
Load image, change it, save it
"""

from PIL import Image, ImageEnhance

import logging

import img_modifier.color_filter as cf
#import img_modifier.blur_filter as bf

logger = logging.getLogger(__name__)


class ImgCommander:
    """
    Class for executing commands for image
    """

    def __init__(self, path):
        if path == "":
            logger.error("path is empty of has bad format")
            raise ValueError("path is empty of has bad format")

        try:
            self._img = Image.open(path)
        except Exception:
            logger.error("can't open the file {0}".format(path))
            raise ValueError("can't open the file {0}".format(path))

    def __str__(self):
        """string representation of an object"""
        return "img {} {} {}".format(self._img.format, "%dx%d" % self._img.size, self._img.mode)

    def resize(self, width, height):
        """resize image"""

        self._img = self._img.resize((width, height))

    def rotate(self, angle):
        """rotate image"""

        self._img = self._img.rotate(angle)

    def blur(self, point, spread):
        """blur image"""

        # todo: add blur module
        pass

    def filter(self, filter_name):
        """filter image"""

        cf.color_filter(self._img, filter_name)

    def brightness(self, factor):
        """adjust image brightness form 0-2 (1 - original)"""

        if factor > 2 or factor < 0:
            raise ValueError("factor should be [0-2]")

        enhancer = ImageEnhance.Brightness(self._img)
        self._img = enhancer.enhance(factor)

    # todo: convert to -100 - +100
    def contrast(self, factor):
        """adjust image contrast form 0.5-1.5 (1 - original)"""

        if factor > 1.5 or factor < 0.5:
            raise ValueError("factor should be [0.5-1.5]")

        enhancer = ImageEnhance.Contrast(self._img)
        self._img = enhancer.enhance(factor)

    def sharpness(self, factor):
        """adjust image sharpness form 0-2 (1 - original)"""

        if factor > 2 or factor < 0:
            raise ValueError("factor should be [0.5-1.5]")

        enhancer = ImageEnhance.Sharpness(self._img)
        self._img = enhancer.enhance(factor)

    def get_img(self):
        """return PIL.Image object"""

        return self._img

    def save(self, path):
        """Save image to hard drive"""

        self._img.save(path)

    def open(self):
        """
        Open image in temporary file
        use it only for debug!
        """

        self._img.open()
