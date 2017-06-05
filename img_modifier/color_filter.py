"""
Apply filters to PIL.image
"""

from PIL import ImageDraw


class ColorFilters:
    items = ("sepia", "negative", "black_white")
    SEPIA, NEGATIVE, BLACK_WHITE = items


def _sepia(img):
    pix = img.load()
    draw = ImageDraw.Draw(img)
    for i in range(img.width):
        for j in range(img.height):
            s = sum(pix[i, j]) // 3
            k = 30
            draw.point((i, j), (s+k*2, s+k, s))


def _black_white(img):
    pix = img.load()
    draw = ImageDraw.Draw(img)
    for i in range(img.width):
        for j in range(img.height):
            s = sum(pix[i, j]) // 3
            draw.point((i, j), (s, s, s))


def _negative(img):
    pix = img.load()
    draw = ImageDraw.Draw(img)
    for i in range(img.width):
        for j in range(img.height):
            draw.point((i, j), (255 - pix[i, j][0], 255 - pix[i, j][1], 255 - pix[i, j][2]))


def color_filter(img, filter_name):
    if filter_name == ColorFilters.SEPIA:
        _sepia(img)
    elif filter_name == ColorFilters.NEGATIVE:
        _negative(img)
    elif filter_name == ColorFilters.BLACK_WHITE:
        _black_white(img)
    else:
        raise ValueError("can't find filter {0}".format(filter_name))
