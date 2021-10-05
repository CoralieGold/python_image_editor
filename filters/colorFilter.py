# ======================================================================================================================
# Built-in imports
# ======================================================================================================================


# ======================================================================================================================
# PythonImageEditing imports
# ======================================================================================================================
from filters import baseFilter


# ======================================================================================================================
# Class
# ======================================================================================================================
class ColorFilter(baseFilter.BaseFilter):
    """ Filter to edit pixels' color. """

    def __init__(self, npImage, color):
        """ Init filter with a numpy array representing an image.

        :param npImage: Image pixels
        :type npImage: :class:`numpy.array`

        :param color: Color to apply to image: (r, g, b)
        :type color: tuple
        """
        self.red = color[0]
        self.green = color[1]
        self.blue = color[2]
        super(ColorFilter, self).__init__(npImage)

    def _pixelCompute(self, x, y):
        """ Compute filter at given image position and return pixel color.

        :param x: X position on source image
        :type x: int

        :param y: Y position on source image
        :type y: int

        :return: Pixel color: (r, g, b)
        :rtype: tuple
        """
        red, green, blue = self.result[x, y]

        return (red * self.red / 255,
                green * self.green / 255,
                blue * self.blue / 255)
