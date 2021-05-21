from BaseTab import BaseTab
from AddVehicle import AddVehicle as AddWidget
from FilterVehicle import FilterVehicle as FilterWidget

from PyQt5.QtCore import pyqtSlot,pyqtSignal

class Vehicles(BaseTab):

    filterSignal = pyqtSignal(str)
    newVehicleSignal = pyqtSignal(int,str,str,str,str,str)

    def __init__(self, parent, interface):
        super(Vehicles, self).__init__(parent=parent, interface=interface)
        self.view = "VehicleView"
        self.table = "Vehicle"
        self.addWidget = AddWidget(self)
        self.filterWidget = FilterWidget(self, self.interface)
        self.connectActions()

    def connectActions(self):
        self.newVehicleSignal.connect(self.addVehicle)
        self.filterSignal.connect(self.filter)
        return super().connectActions()

    @pyqtSlot(str)
    def filter(self, mID):
        self.interface.filterVehicle(mID)

    @pyqtSlot(int,str,str,str,str,str)
    def addVehicle(self,id,make, model, year, color, miles):
        if id!=0:
            makeID = self.interface.checkExist("Manufacturer", "Name", make)
            if makeID == 0:
                row = {"Make":make}
                makeID = self.interface.insertMake(row, commit = False)
            modelID = self.interface.checkExist("Model", "Name", model)
            if modelID == 0:
                row = {"Model":model}
                modelID = self.interface.insertModel(row, makeID, commit = False)
            row = {"ID":id, "Year":year, "Color":color, "Miles": miles}
            vehicleID = self.interface.updateVehicle(row, modelID, commit = True)
            self.addWidget.hide()
        else:
            makeID = self.interface.checkExist("Manufacturer", "Name", make)
            if makeID == 0:
                row = {"Make":make}
                makeID = self.interface.insertMake(row, commit = False)
            modelID = self.interface.checkExist("Model", "Name", model)
            if modelID == 0:
                row = {"Model":model}
                modelID = self.interface.insertModel(row, makeID, commit = False)
            row = {"Year":year, "Color":color, "Miles": miles}
            vehicleID = self.interface.insertVehicle(row, modelID, commit = True)
            self.addWidget.hide()
        return
    
    @pyqtSlot()
    def updateEntry(self):
        if self.parent.tableView.selectedIndexes():
            self.addWidget.addButton.setText("Update")
            self.parent.tableView.showColumn(0)
            idx = self.parent.tableView.selectedIndexes()[0].data()
            self.parent.tableView.hideColumn(0)
            self.addWidget.updateEnt(self.interface.fetch(idx,self.view))