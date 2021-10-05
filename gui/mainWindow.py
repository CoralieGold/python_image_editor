# ======================================================================================================================
# Built-in imports
# ======================================================================================================================


# ======================================================================================================================
# Qt imports
# ======================================================================================================================
from PyQt5 import QtWidgets
from PyQt5 import QtGui


# ======================================================================================================================
# Tool imports
# ======================================================================================================================
from utils import ioUtils
from filters import colorFilter
from filters import parameterFilter


# ======================================================================================================================
# Global Variables definition
# ======================================================================================================================
DEFAULT_HEIGHT = 200


# ======================================================================================================================
# Python Image Editing main Window
# ======================================================================================================================
class PythonImageEditingWindow(QtWidgets.QMainWindow):
    """ Main PythonImageEditing tool Window """

    def __init__(self, parent=None):
        super(PythonImageEditingWindow, self).__init__(parent)

        self.imagePath = ''
        self.npImage = None
        self.allFilters = []
        self.filterIndex = -1

        self._initUI()

    def _initUI(self):
        """ Init User Interface:
            - Menu bar
            - Viewer
            - Action buttons
        """
        self.setWindowTitle('Python Image Editing')
        self.setGeometry(300, 300, 300, 200)

        self.mainLayout = QtWidgets.QVBoxLayout()
        mainWidget = QtWidgets.QWidget()
        mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(mainWidget)

        self._initUIToolBarFile()
        self._initUIToolBarFilters()
        self._initUIToolBarOptions()

        self.imageViewer = QtWidgets.QLabel()
        self.mainLayout.addWidget(self.imageViewer)

    def _initUIToolBarFile(self):
        """ Initialize File ToolBar:
            - Open Image
            - Save Image
        """
        fileToolBar = self.addToolBar('File')

        openImageAction = QtWidgets.QAction(QtGui.QIcon('gui/icons/add_sq.png'), '&Open Image', self)
        openImageAction.triggered.connect(self._onOpenImageClicked)
        fileToolBar.addAction(openImageAction)

        saveImageAction = QtWidgets.QAction(QtGui.QIcon('gui/icons/save_1.png'), '&Save Image', self)
        saveImageAction.triggered.connect(self._onSaveImageClicked)
        fileToolBar.addAction(saveImageAction)

    def _initUIToolBarFilters(self):
        """ Initialize Filters ToolBar:
            - Color Filter
            - Contrast Filter
        """
        filtersToolBar = self.addToolBar('Filters')

        colorFilterAction = QtWidgets.QAction('&Color Filter', self)
        colorFilterAction.triggered.connect(self._onColorFilterClicked)
        filtersToolBar.addAction(colorFilterAction)

        contrastFilterAction = QtWidgets.QAction('&Contrast Filter', self)
        contrastFilterAction.triggered.connect(self._onContrastFilterClicked)
        filtersToolBar.addAction(contrastFilterAction)

    def _initUIToolBarOptions(self):
        optionsToolBar = self.addToolBar('Options')
        self.undoAction = QtWidgets.QAction('&<', self)
        self.undoAction.triggered.connect(self._onUndoActionClicked)
        self.undoAction.setEnabled(False)
        optionsToolBar.addAction(self.undoAction)

        self.doAction = QtWidgets.QAction('&>', self)
        self.doAction.triggered.connect(self._onDoActionClicked)
        self.doAction.setEnabled(False)
        optionsToolBar.addAction(self.doAction)

    def _onOpenImageClicked(self):
        """ Function called when Open Image button clicked. """
        self.imagePath, _ = QtWidgets.QFileDialog.getOpenFileName(caption='Open file',
                                                                  filter='Image files (*.jpg *.gif *.png)')
        self.npImage = ioUtils.readImage(self.imagePath, (None, DEFAULT_HEIGHT))
        self.displayImage()

    def _onSaveImageClicked(self):
        """ Function called when Save Image button clicked. """
        npOriginalImage = ioUtils.readImage(self.imagePath)

        for imageFilter in self.allFilters:
            print("Apply: ", imageFilter)
            imageFilter.source = npOriginalImage
            npOriginalImage = imageFilter.apply()

        ioUtils.saveImage(npOriginalImage, self.imagePath)
        print('Image Saved')

    def _applyFilter(self, imageFilter):
        """ Apply given filter to current npImage.

        :param imageFilter: Filter to apply to image
        :type imageFilter: :class:`filters.baseFilter.BaseFilter`
        """
        self.npImage = imageFilter.apply()
        self.displayImage()
        if imageFilter not in self.allFilters:
            self.allFilters.append(imageFilter)
        self.filterIndex += 1
        self.doAction.setEnabled(False)
        self.undoAction.setEnabled(True)

    def _unApplyFilter(self, imageFilter):
        self.npImage = imageFilter.unApply()
        self.displayImage()
        self.filterIndex -= 1
        self.undoAction.setEnabled(self.filterIndex > 0)
        self.doAction.setEnabled(True)

    def _onColorFilterClicked(self):
        """ Function called when Color Filter Action clicked. """
        color = QtWidgets.QColorDialog.getColor()
        self._applyFilter(colorFilter.ColorFilter(self.npImage,
                                                  (color.red(), color.green(), color.blue())))

    def _onContrastFilterClicked(self):
        """ Function called when Color Filter Action clicked. """
        intensity = 20
        self._applyFilter(parameterFilter.ContrastFilter(self.npImage, intensity))

    def _onDoActionClicked(self):
        self._applyFilter(self.allFilters[self.filterIndex])

    def _onUndoActionClicked(self):
        self._unApplyFilter(self.allFilters[self.filterIndex])

    def displayImage(self):
        """ Display image numpy array as a pixmap. """
        if self.npImage is None:
            print('No np image found')
            return

        height, width, channel = self.npImage.shape
        qImg = QtGui.QImage(self.npImage.data, width, height, 3 * width, QtGui.QImage.Format_RGB888)
        self.imageViewer.setPixmap(QtGui.QPixmap(qImg))
