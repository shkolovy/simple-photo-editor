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

from img_modifier import img_commander

logger = logging.getLogger(__name__)


def init():
    """Get parameters form console"""

    args = sys.argv[1:]

    if len(args) == 0:
        logger.error("-p can't be empty")
        raise ValueError("-p can't be empty")

    # transform arguments from console
    opts, rem = getopt.getopt(args, "p:", ["rotate=", "resize=", "color_filter="])
    rotate = resize = color_filter = None

    for opt, arg in opts:
        if opt == "-p":
            path = arg
        elif opt == "--rotate":
            rotate = int(arg)
        elif opt == "--resize":
            resize = arg
        elif opt == "--color_filter":
            color_filter = arg

    image = img_commander.ImgCommander(path)
    if rotate:
        image.rotate(rotate)
    if resize:
        w, h = map(int, arg.split(','))
        image.resize(w, h)
    if color_filter:
        image.filter(color_filter)

    if __debug__:
        # image.contrast(2)
        # image.brightness(0.5)
        image.sharpness(5)
        image.get_img().show()


if __name__ == "__main__":
    init()
