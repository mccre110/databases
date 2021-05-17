from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

class FilterInvoice(QtWidgets.QDialog):

    def __init__(self, parent, interface):
        super(FilterInvoice, self).__init__(parent=parent)
        uic.loadUi("GUI//filterInvoice.ui", self)
        self.parent = parent
        self.interface = interface
        self.connectActions()
    
    def connectActions(self):
        self.filterButton.clicked.connect(self.filterInvoice)

    def filterInvoice(self):
        self.parent.filterSignal.emit(
            self.cbMechanic.currentData(),
            self.cbVehicle.currentData()
        )
    
    def showEvent(self, event):
        for index, row in self.interface.getMechList().iterrows():
            self.cbMechanic.addItem(str(row['Name']), index)
        for index, row in self.interface.getVList().iterrows():
            data = str(row['Year']) +" "+ row['Make'] +" "+ row['Model']
            self.cbVehicle.addItem(data, index)
        self.cbMechanic.insertItem(0,"----", -1)
        self.cbMechanic.setCurrentIndex(0)
        self.cbVehicle.insertItem(0,"----", -1)
        self.cbVehicle.setCurrentIndex(0)
        super().showEvent(event)
    
    def hideEvent(self, event):
        self.cbMechanic.clear()
        self.cbVehicle.clear()
        return super().hideEvent(event)