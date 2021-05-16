# https://stackoverflow.com/questions/31475965/fastest-way-to-populate-qtableview-from-pandas-data-frame
from PyQt5 import QtGui, QtCore

class PandasTableModel(QtGui.QStandardItemModel):
    def __init__(self, data, parent=None):
        QtGui.QStandardItemModel.__init__(self, parent)
        self._data = data

        for col in data.columns:
            data_col = [QtGui.QStandardItem("{}".format(x)) for x in data[col].values]
            self.appendColumn(data_col)
        return

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def headerData(self, x, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[x]
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return self._data.index[x]
        return None
    
    # def itemChanged(self, item: 'QStandardItem') -> None:
    #     return super().itemChanged(item)

    # """
    # Class to populate a table view with a pandas dataframe
    # """
    # def __init__(self, data, parent=None):
    #     QtCore.QAbstractTableModel.__init__(self, parent)
    #     self._data = data

    # def rowCount(self, parent=None):
    #     return len(self._data.values)

    # def columnCount(self, parent=None):
    #     return self._data.columns.size

    # def data(self, index, role=QtCore.Qt.DisplayRole):
    #     if index.isValid():
    #         if role == QtCore.Qt.DisplayRole:
    #             return str(self._data.iloc[index.row()][index.column()])
    #     return None

    # def headerData(self, rowcol, orientation, role):         
    #     if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:             
    #         return self._data.columns[rowcol]         
    #     if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole: 
    #                 return self._data.index         
    #     return None