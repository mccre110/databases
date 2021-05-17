from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

class FilterVehicle(QtWidgets.QDialog):

    def __init__(self, parent, interface):
        super(FilterVehicle, self).__init__(parent=parent)
        uic.loadUi("GUI//filterVehicle.ui", self)
        self.parent = parent
        self.interface = interface
        self.connectActions()
    
    def connectActions(self):
        self.filterButton.clicked.connect(self.filterVehicle)

    def filterVehicle(self):
        self.parent.filterSignal.emit(self.cbMake.currentText())
    
    def showEvent(self, event):
        for index, row in self.interface.getMakeList().iterrows():
            self.cbMake.addItem(str(row['Name']), index)
        super().showEvent(event)
    
    def hideEvent(self, event):
        self.cbMake.clear()
        return super().hideEvent(event)