# ======================================================================================================================
# Built-in imports
# ======================================================================================================================
import os
import numpy as np
from PIL import Image


# ======================================================================================================================
# Functions
# ======================================================================================================================
def readImage(imagePath, size=(None, None)):
    """ Use PIL to get an numpy array of given image path.

    :param imagePath: Path to an image file.
    :type imagePath: str

    :param size: Use these width and height to resize image. If one is None, use ratio for to compute it.
    :type size: tuple

    :return: Numpy array describing an image with pixels.
    :rtype: :class:`numpy.array`
    """
    if not os.path.exists(imagePath):
        print('Path doesnt exist')
        raise ValueError

    pilImage = Image.open(imagePath)

    width = size[0]
    height = size[1]

    if width or height:
        sourceWidth = pilImage.size[0]
        sourceHeight = pilImage.size[1]

        if not width:
            width = sourceWidth * (height/sourceHeight)
        elif not height:
            height = sourceHeight * (width/sourceWidth)

        pilImage.thumbnail((width, height), Image.ANTIALIAS)

    return pilImageToNpArray(pilImage)


def saveImage(npImage, filePath):
    """ Save numpy array describing an image as a real image using given filePath.

    :param npImage: Numpy array describing an image with pixels.
    :type npImage: :class:`numpy.array`

    :param filePath: Save image on this file path.
    :type filePath: str
    """
    pilImage = npArrayToPilImage(npImage)
    pilImage.save(filePath)


def pilImageToNpArray(pilImage):
    """ Convert PIL image to numpy array.

    :param pilImage: PIL Image to convert.
    :type pilImage: :class:`PIL.Image`

    :return: Numpy array describing given PIL Image.
    :rtype: :class:`numpy.array`
    """
    return np.array(pilImage)


def npArrayToPilImage(npImage):
    """ Convert numpy array to PIL image.


    :param npImage: Numpy array to convert.
    :type npImage: :class:`numpy.array`

    :return: PIL Image describing given numpy array.
    :rtype: :class:`PIL.Image`
    """
    return Image.fromarray(npImage)
