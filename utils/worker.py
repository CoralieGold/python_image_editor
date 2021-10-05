from PyQt5 import QtCore
import traceback
import sys


class Worker(QtCore.QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''
    FINISHED = QtCore.pyqtSignal()
    ERROR = QtCore.pyqtSignal(tuple)
    RESULT = QtCore.pyqtSignal(object)
    PROGRESS = QtCore.pyqtSignal(int)

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @QtCore.pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.ERROR.emit((exctype, value, traceback.format_exc()))
        else:
            self.RESULT.emit(result)  # Return the result of the processing
        finally:
            self.FINISHED.emit()  # Done
