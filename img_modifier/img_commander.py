"""
Load image, change it, save it
"""

from PIL import Image
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

    def get_img(self):
        """returns img object"""

        return self._img

    def save(self, path):
        """Save image"""

        self._img.save(path)

    def open(self):
        """Open image"""

        self._img.open()

