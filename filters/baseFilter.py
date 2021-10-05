# ======================================================================================================================
# Built-in imports
# ======================================================================================================================
import numpy as np


# ======================================================================================================================
# Filter class
# ======================================================================================================================
class BaseFilter(object):
    """ Class representing a filter to apply in an image. """

    def __init__(self, npImage):
        """ Init filter with a numpy array representing an image.

        :param npImage: Image pixels
        :type npImage: :class:`numpy.array`
        """
        super(BaseFilter, self).__init__()
        self.source = npImage
        self.result = None

    def apply(self):
        """ Apply filter to image pixels.

        :return: Image with filter applied
        :rtype: :class:`numpy.array`
        """
        self.result = np.copy(self.source)

        for x in range(self.result.shape[0]):
            for y in range(self.result.shape[1]):
                self.result[x, y] = self._pixelCompute(x, y)

        return self.result

    def unApply(self):
        return self.source

    def _pixelCompute(self, x, y):
        """ Compute filter at given image position and return pixel color.

        :param x: X position on source image
        :type x: int

        :param y: Y position on source image
        :type y: int

        :return: Pixel color: (r, g, b)
        :rtype: tuple
        """
        return self.source[x, y]
