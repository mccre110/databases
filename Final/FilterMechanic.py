from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

class FilterMechanic(QtWidgets.QDialog):

    def __init__(self, parent, interface):
        super(FilterMechanic, self).__init__(parent=parent)
        uic.loadUi("filterMechanic.ui", self)
        self.parent = parent
        self.interface = interface
        self.connectActions()
    
    def connectActions(self):
        self.filterButton.clicked.connect(self.filterMechanic)

    def filterMechanic(self):
        self.parent.filterSignal.emit(self.leAddress.text())