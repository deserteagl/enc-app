from PyQt5 import QtCore, QtGui, QtWidgets

class File_ui_add(QtWidgets.QFileDialog):
    def __init__(self,parent):
        super().__init__(parent)
        self.setModal(True)

