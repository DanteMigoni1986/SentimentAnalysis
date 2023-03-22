from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt

class TopWordsModel(QtCore.QAbstractListModel):
    def __init__(self, words = None):
        super().__init__()
        self.words = words or []
        
    def data(self, index, role):
        if role == Qt.DisplayRole:
            text = self.words[index.row()]
            return text
        
    def rowCount(self, index):
        return len(self.words)
        