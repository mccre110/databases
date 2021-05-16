from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

class AddInvoice(QtWidgets.QDialog):

    def __init__(self, parent, interface):
        super(AddInvoice, self).__init__(parent=parent)
        uic.loadUi("addInvoice.ui", self)
        self.parent = parent
        self.interface = interface
        self.ID = 0

        self.connectActions()
    
    def connectActions(self):
        self.addButton.clicked.connect(self.sendInvoice)
    
    def showEvent(self, event):
        for index, row in self.interface.getMechList().iterrows():
            self.cbMechanic.addItem(str(row['Name']), index)
        for index, row in self.interface.getVList().iterrows():
            data = str(row['Year']) +" "+ row['Make'] +" "+ row['Model']
            self.cbVehicle.addItem(data, index)
        super().showEvent(event)
    
    def hideEvent(self, event):
        self.deDate.clear()
        self.leAmount.clear()
        self.tbDescription.clear()
        self.leOdo.clear()
        self.cbMechanic.clear()
        self.cbVehicle.clear()
        return super().hideEvent(event)

    @pyqtSlot()
    def sendInvoice(self):
        self.parent.newInvoiceSignal.emit(
            self.ID,
            self.deDate.text(),
            self.leAmount.text(),
            self.tbDescription.toPlainText(),
            self.leOdo.text(),
            self.cbMechanic.currentData(),
            self.cbVehicle.currentData()
        )
        self.ID = 0

    def updateEnt(self,data):
        self.show()
        self.ID = data["ID"].values[0]
        self.deDate.setDate(data["Date"].values[0])
        self.leAmount.setText(str(data["Amount"].values[0]))
        self.tbDescription.setPlainText(data["Description"].values[0])
        self.leOdo.setText(str(data["Odometer"].values[0]))
        self.cbMechanic.setCurrentIndex(self.cbMechanic.findData(int(data["MechanicID"].values[0])))
        self.cbVehicle.setCurrentIndex(self.cbVehicle.findData(int(data["VehicleID"].values[0])))