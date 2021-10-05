import sys
from PyQt5 import QtWidgets
from gui import mainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mainWindow.PythonImageEditingWindow()
    window.show()
    sys.exit(app.exec_())
