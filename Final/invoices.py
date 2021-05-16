from BaseTab import BaseTab
from AddInvoice import AddInvoice as AddWidget
from FilterInvoice import FilterInvoice as FilterWidget

from PyQt5.QtCore import pyqtSlot,pyqtSignal

class Invoices(BaseTab):

    filterSignal = pyqtSignal(int,int)
    newInvoiceSignal = pyqtSignal(int,str,str,str,str,int,int)

    def __init__(self, parent, interface):
        super(Invoices, self).__init__(parent=parent, interface=interface)
        self.view = "InvoiceView"
        self.table = "Invoice"
        self.addWidget = AddWidget(self, self.interface)
        self.filterWidget = FilterWidget(self, self.interface)
        self.connectActions()

    def connectActions(self):
        self.newInvoiceSignal.connect(self.addInvoice)
        self.filterSignal.connect(self.filter)
        return super().connectActions()

    @pyqtSlot(int,int)
    def filter(self, mech, veh):
        self.interface.filterInvoice(mech,veh)

    @pyqtSlot(int,str,str,str,str,int, int)
    def addInvoice(self,id,date, amount, des, odo, mechanic, vehicle):
        if id!=0:
            row= {"ID":id,"Date":date, "Amount": amount, "Desc": des, "Odo":odo}
            _ = self.interface.updateInvoice(row, mechanic, vehicle)
            self.addWidget.hide()
        else:
            row= {"Date":date, "Amount": amount, "Desc": des, "Odo":odo}
            _ = self.interface.insertInvoice(row, mechanic, vehicle)
            self.addWidget.hide()
        return
    
    