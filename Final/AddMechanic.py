from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

class AddMechanic(QtWidgets.QDialog):

    def __init__(self, parent):
        super(AddMechanic, self).__init__(parent=parent)
        uic.loadUi("GUI//addMechanic.ui", self)
        self.parent = parent
        self.ID = 0
        
        self.connectActions()
    
    def connectActions(self):
        self.addButton.clicked.connect(self.sendMechanic)
    
    def hideEvent(self, event):
        self.leName.clear()
        self.lePhone.clear()
        self.leAddress.clear()
        return super().hideEvent(event)

    @pyqtSlot()
    def sendMechanic(self):
        self.parent.newMechanicSignal.emit(
            self.ID,
            self.leName.text(),
            self.lePhone.text(),
            self.leAddress.text()
        )
        self.ID = 0

    def updateEnt(self,data):
        self.show()
        self.ID = data["ID"].values[0]
        self.leName.setText(data["Name"].values[0])
        self.lePhone.setText(str(data["PhoneNumber"].values[0]))
        self.leAddress.setText(data["Address"].values[0])