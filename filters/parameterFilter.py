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
class ContrastFilter(baseFilter.BaseFilter):
    """ Filter to edit pixels' color. """

    def __init__(self, npImage, intensity):
        """ Init filter with a numpy array representing an image.

        :param npImage: Image pixels
        :type npImage: :class:`numpy.array`

        :param intensity: Contrast intensity
        :type intensity: int
        """
        super(ContrastFilter, self).__init__(npImage)
        self.intensity = intensity

    def _pixelCompute(self, x, y):
        """ Compute filter at given image position and return pixel color.

        :param x: X position on source image
        :type x: int

        :param y: Y position on source image
        :type y: int

        :return: Pixel color: (r, g, b)
        :rtype: tuple
        """
        pixelResult = []

        for color in self.result[x, y]:
            color = color + self.intensity if color > 128 else color - self.intensity
            if color < 0:
                color = 0
            elif color > 255:
                color = 255

            pixelResult.append(color)

        return pixelResult
