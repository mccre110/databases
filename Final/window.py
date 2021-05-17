import sys
import os

try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    pass

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5 import QtWidgets
from PyQt5 import uic
from pandas.core.frame import DataFrame

import invoices
import vehicles
import mechanics
import interface
import PandasModel

class Window(QtWidgets.QWidget):

    logSignal = pyqtSignal(str)
    viewSignal = pyqtSignal(DataFrame)
    
    def __init__(self, parent):
        super(Window, self).__init__(parent=parent)
        uic.loadUi("GUI//master.ui", self)
        self.setWindowTitle("Auto Maintenance Logger")
        self.parent = parent
        self.interface = interface.Interface(self)

        self.vehicles = vehicles.Vehicles(self,self.interface)
        self.tabWidget.addTab(self.vehicles, "Vehicles")

        self.mechanics = mechanics.Mechanics(self,self.interface)
        self.tabWidget.addTab(self.mechanics, "Mechanics")

        self.invoices = invoices.Invoices(self,self.interface)
        self.tabWidget.addTab(self.invoices, "Invoices")

        self.connectActions()

    def connectActions(self):
        self.logSignal.connect(self.appendLog)
        self.viewSignal.connect(self.updateView)
        self.reportButton.clicked.connect(self.report)

    @pyqtSlot()
    def report(self):
        if self.interface.generateReports():
            QtWidgets.QMessageBox.information(self,"Report", "Sucessfully Genreated", QtWidgets.QMessageBox.Ok)

    @pyqtSlot(str)
    def appendLog(self, text):
        self.listWidget.addItem(text)

    @pyqtSlot(DataFrame)
    def updateView(self, data):
        model = PandasModel.PandasTableModel(data)
        self.tableView.setModel(model)
        self.tableView.hideColumn(0)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    win = Window(None)
    win.show()
    sys.exit(app.exec())