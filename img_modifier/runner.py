"""
Command line usage:
    python3 runner.py [-p <path>] [--rotate=<angle>] [--resize=<width,height>] [--color_filter=<filter_name>]

    example: python3 runner.py -p temp.jpg --rotate=45 --resize=200,300

Options:
  -p path:  path to initial image
  --rotate: rotate image to N degrees
  --resize: resize image to W and H
  --color_filter: apply color filter (sepia, black_white, negative)
"""

import getopt
import sys
import logging

from img_modifier import img_helper

logger = logging.getLogger()


def init():
    """Get parameters form console"""

    args = sys.argv[1:]

    if len(args) == 0:
        logger.error("-p can't be empty")
        raise ValueError("-p can't be empty")

    logger.debug(f"run with params: {args}")

    # transform arguments from console
    opts, rem = getopt.getopt(args, "p:", ["rotate=", "resize=", "color_filter="])
    rotate_angle = resize = color_filter = None

    for opt, arg in opts:
        if opt == "-p":
            path = arg
        elif opt == "--rotate":
            rotate_angle = int(arg)
        elif opt == "--resize":
            resize = arg
        elif opt == "--color_filter":
            color_filter = arg

    img = img_helper.get_img(path)
    if rotate_angle:
        img = img_helper.rotate(img, rotate_angle)
    if resize:
        w, h = map(int, arg.split(','))
        img = img_helper.resize(img, w, h)
    if color_filter:
        img = img_helper.color_filter(img, color_filter)

    if __debug__:
        img.show()


if __name__ == "__main__":
    init()
