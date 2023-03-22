import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig = plt.figure(figsize = (10, 5))  # Posible argumento: figsize=(5, 4), dpi=200
        super().__init__(fig)
        self.setParent(parent)
        self.data = {}
        self.sentiments = list(self.data.keys())
        self.values = list(self.data.values())
        
    def populateBarPlot(self):
        plt.bar(self.sentiments, self.values, color ='maroon', width = 0.4)