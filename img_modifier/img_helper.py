"""
Load image, change it, save it
"""

from PIL import Image, ImageEnhance
import logging

import img_modifier.color_filter as cf

logger = logging.getLogger(__name__)


def get_img(path):
    """return PIL.Image object"""

    if path == "":
        logger.error("path is empty of has bad format")
        raise ValueError("path is empty of has bad format")

    try:
        return Image.open(path)
    except Exception:
        logger.error("can't open the file {0}".format(path))
        raise ValueError("can't open the file {0}".format(path))


def resize(img, width, height):
    """resize image"""

    return img.resize((width, height))


def rotate(img, angle):
    """rotate image"""

    return img.rotate(angle)


def blur(img, point, spread):
    """blur image"""

    # todo: add blur module
    pass


def color_filter(img, filter_name):
    """filter image"""

    return cf.color_filter(img, filter_name)


def brightness(img, factor):
    """adjust image brightness form 0.5-2 (1 - original)"""

    if factor > 2 or factor < 0.5:
        raise ValueError("factor should be [0-2]")

    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)


def contrast(img, factor):
    """adjust image contrast form 0.5-1.5 (1 - original)"""

    if factor > 1.5 or factor < 0.5:
        raise ValueError("factor should be [0.5-1.5]")

    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(factor)


def sharpness(img, factor):
    """adjust image sharpness form 0-2 (1 - original)"""

    if factor > 2 or factor < 0:
        raise ValueError("factor should be [0.5-1.5]")

    enhancer = ImageEnhance.Sharpness(img)
    return enhancer.enhance(factor)


def flip_left(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)


def flip_top(img):
    return img.transpose(Image.FLIP_TOP_BOTTOM)


def save(img, path):
    """Save image to hard drive"""

    img.save(path)


def open_img(img):
    """
    Open image in temporary file
    use it only for debug!
    """

    img.open()
