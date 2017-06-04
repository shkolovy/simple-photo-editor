"""
Command line usage:
    python3 img_modifier.py [-p <path>] [--rotate=<angle>] [--resize=<width,height>]

    example1: python3 img_modifier.py -p temp.jpg --rotate=45 --resize=200,300
    example2:
        python3
        >>from img_modifier import ImgModifier as im
        >>img = im("temp.jpg")
        >>img.resize(100, 100)
        >>img.open()

Options:
  -p path: path to initial image
  --rotate: rotate image to N degrees
  --resize: resize image to W and H
"""

from PIL import Image
import getopt
import sys

from logging.config import fileConfig
import logging


class ImgModifier:
    """
    Class for modifying image
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

    def filter(self, name):
        """filter image"""

        # todo: add filter module
        pass

    def get_img(self):
        """returns img object"""

        return self._img

    def save(self, path):
        """Save image"""

        self._img.save(path)

    def open(self):
        """Open image"""

        self._img.open()


def init():
    """Process parameters form console"""

    args = sys.argv[1:]

    if len(args) == 0:
        logger.error("-p can't be empty")
        raise ValueError("-p can't be empty")

    # transform arguments from console
    opts, rem = getopt.getopt(args, "p:", ["rotate=", "resize="])

    for opt, arg in opts:
        if opt == "-p":
            path = arg
        elif opt == "--rotate":
            rotate = int(arg)
        elif opt == "--resize":
            resize = arg

    image = ImgModifier(path)
    if rotate:
        image.rotate(rotate)
    if resize:
        w, h = map(int, arg.split(','))
        image.resize(w, h)

    image.get_img().show()


if __name__ == "__main__":
    # init logger from config file
    fileConfig('logging_config.ini')
    logger = logging.getLogger()

    init()
