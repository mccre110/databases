from BaseTab import BaseTab
from AddMechanic import AddMechanic as AddWidget
from FilterMechanic import FilterMechanic as FilterWidget

from PyQt5.QtCore import pyqtSlot,pyqtSignal

class Mechanics(BaseTab):

    filterSignal = pyqtSignal(str)
    newMechanicSignal = pyqtSignal(int,str,str,str)

    def __init__(self, parent, interface):
        super(Mechanics, self).__init__(parent=parent, interface=interface)
        self.view = "MechanicView"
        self.table = "Mechanic"
        self.addWidget = AddWidget(self)
        self.filterWidget = FilterWidget(self, self.interface)
        self.connectActions()

    def connectActions(self):
        self.newMechanicSignal.connect(self.addMechanic)
        self.filterSignal.connect(self.filter)
        return super().connectActions()
    
    @pyqtSlot(str)
    def filter(self, add):
        add = '%'+add+'%'
        self.interface.filterMechanic(add)
    
    @pyqtSlot(int,str,str,str)
    def addMechanic(self, id, name, phone, address):
        if id!=0:
            mechID = self.interface.checkExist("Mechanic","Name", name)
            if mechID == 0:
                row = {"ID": id, "Name":name, "Phone":phone, "Address": address}
                mechID = self.interface.updateMechanic(row)
            self.addWidget.hide()
        else:
            mechID = self.interface.checkExist("Mechanic","Name", name)
            if mechID == 0:
                row = {"Name":name, "Phone":phone, "Address": address}
                mechID = self.interface.insertMechanic(row)
            self.addWidget.hide()
        return