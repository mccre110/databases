import sys
import os

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

class BaseTab(QtWidgets.QWidget):

    def __init__(self, parent, interface):
        super(BaseTab, self).__init__(parent=parent)
        uic.loadUi("tab.ui", self)
        self.parent = parent
        self.interface = interface


    def connectActions(self):
        # self.showEvent.connect()
        self.addWidget.setWindowTitle(self.table)
        self.updateButton.clicked.connect(lambda state, tableName=self.view: self.interface.getAll(tableName))
        self.deleteButton.clicked.connect(self.deleteEntry)
        self.editButton.clicked.connect(self.updateEntry)
        self.addButton.clicked.connect(self.addEntry)
        self.filterButton.clicked.connect(self.filterWidget.show)

    def showEvent(self, event):
        self.interface.getAll(self.view)
        super().showEvent(event)
    
    @pyqtSlot()
    def addEntry(self):
        self.addWidget.addButton.setText("Add")
        self.addWidget.repaint()
        self.addWidget.show()

    @pyqtSlot()
    def updateEntry(self):
        if self.parent.tableView.selectedIndexes():
            self.addWidget.addButton.setText("Update")
            self.parent.tableView.showColumn(0)
            idx = self.parent.tableView.selectedIndexes()[0].data()
            self.parent.tableView.hideColumn(0)
            self.addWidget.updateEnt(self.interface.fetch(idx,self.table))

    @pyqtSlot()
    def deleteEntry(self):
        self.parent.tableView.showColumn(0)
        idx = self.parent.tableView.selectedIndexes()[0].data()
        self.parent.tableView.hideColumn(0)
        self.interface.softDelete(idx,self.table)