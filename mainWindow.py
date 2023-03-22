from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic, QtSerialPort, QtCore
from tweetAnalyzer import TweetAnalyzer
from graph_plot import Canvas
from topWordsModel import TopWordsModel


class MainApp(QMainWindow):
    botonPresionado = pyqtSignal()
    
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent=parent)
        uic.loadUi('interface.ui', self)
        layout = QVBoxLayout()
        self.chart = Canvas(self)
        self.index=0
        layout.addWidget(self.chart)
        self.graphContainer.setLayout(layout)
        self.tweetAnalyzer = TweetAnalyzer([])
        self.populateGraph()
        self.model = TopWordsModel()
        self.listView.setModel(self.model)
        self.getTopWords()
        
    def getTopWords(self):
        topWords = self.tweetAnalyzer.fetchMostPopularWords()
        self.model.words = []
        i = 1
        
        for word in topWords:
            if word[0] != '' and word[0] != ' ' and word[0] != 'rt' and i < 16:
                self.model.words.append((str(i)+'.- '+word[0]+' - '+str(word[1])))
                i = i + 1
        
    def populateGraph(self):
        positivismo = self.tweetAnalyzer.fetchAveragePositiveReaction()
        negatividad = self.tweetAnalyzer.fetchAverageNegativeReaction()
        subjetividad = self.tweetAnalyzer.fetchAverageSubjectiveReaction()
        ordenados = self.sentimientoMasIntenso([subjetividad, positivismo, negatividad])
        self.sentimientoIntenso.setText("¿Qué sentimiento es más intenso? Positivismo")
        self.objetividadTema.setText("¿Qué tan objetivos son los Tweets sobre el tema? La subjetividad es pequeña, podemos concluir que son "+str(round((1-subjetividad)*100,2))+"% objetivos")
        self.positivismoTema.setText("¿Qué tan positivos se espera que sean los comentarios para el día de mañana? Se espera que sean "+str(round((positivismo)*100,2))+"% positivos")
        self.chart.data = {'Positivismo': positivismo, 'Negatividad': negatividad, 'Subjetividad': subjetividad}
        self.chart.sentiments = list(self.chart.data.keys())
        self.chart.values = list(self.chart.data.values())
        self.chart.populateBarPlot()

    def sentimientoMasIntenso(self, numbers):
        return sorted(numbers)
        
    

if __name__ == '__main__':        
    app = QApplication([])              # Si no recibe argumentos de la consola de comandos, se escribe con [] vacíos
    window = MainApp()                  # Se establece una ventana principal para arrancar
    window.show()                       # Muestra la ventana principal (por default se encuentran ocultas)
    app.exec_()                         # Inicia un ciclo de eventos que no se cierra hasta que el usuario lo indique