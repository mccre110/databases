from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

class AddVehicle(QtWidgets.QDialog):

    def __init__(self, parent):
        super(AddVehicle, self).__init__(parent=parent)
        uic.loadUi("GUI//addVehicle.ui", self)
        self.parent = parent
        self.ID = 0

        self.connectActions()
    
    def connectActions(self):
        self.addButton.clicked.connect(self.sendVehicle)
    
    def hideEvent(self, event):
        self.leMake.clear()
        self.leModel.clear()
        self.leYear.clear()
        self.leColor.clear()
        self.leMiles.clear()
        return super().hideEvent(event)
    
    @pyqtSlot()
    def sendVehicle(self):
        self.parent.newVehicleSignal.emit(
            self.ID,
            self.leMake.text(),
            self.leModel.text(),
            self.leYear.text(),
            self.leColor.text(),
            self.leMiles.text()
        )
        self.ID = 0
    
    def updateEnt(self,data):
        self.show()
        self.ID = data["ID"].values[0]
        self.leMake.setText(data["Make"].values[0])
        self.leModel.setText(data["Model"].values[0])
        self.leYear.setText(str(data["Year"].values[0]))
        self.leColor.setText(data["Color"].values[0])
        self.leMiles.setText(str(data["Miles"].values[0]))