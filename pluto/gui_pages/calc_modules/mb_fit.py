"""
Klasse zum Fitten einer Maxwell-Boltzmann Verteilung aus puck Daten 
die im .pkl format vorliegen müssen
"""
__author__ = 'Claas Fillies, Friedrich Rieber'
__version__ = '1.0'


import numpy as np
import cv2 as cv
import sys
import math
import matplotlib.pyplot as plt
import matplotlib
from scipy.optimize import curve_fit


class MbFit:
    """
    Klasse zum Fitten von einer Maxwell Boltzmann Verteilung auf bereits
    existierende Puck Daten.
    """

    aldkeys = list()
    aldvalue = list()
    # Als listen initialiesiert weil noch unbekannt was es genau ist
    x = list()
    parameter = list()

    def __init__(self):
        """
        Konsturktor der MbFit Klasse welcher die einzelnen Schritte des
        Vorgangs einzeln aufruft
        """
        global dxylist 
        dxylist = list()

    def calc_and_fit(self):
        """
        Funktion die die einzelnen nötigen Schritte ausführt
        """
        self.calcucalte_velocitys()
        self.count_velocity()
        self.fit()

    def load_puck_data(self, all_data_boxes):
        """
        Läd Puck Daten entweder über ein Argument oder einen 
        festgelegten Pfad und Speicher es in all_boxes
        """
        global all_boxes 
        all_boxes = all_data_boxes

    def calcucalte_velocitys(self):
        """
        Berechnet die Geschwindigkeiten aus den Positionsdaten speichert
        sie in dxylist und sortiert sie.
        """
        i2 = 0
        ax = 0
        ay = 0
        dxy = 0
        alteX = list()
        alteY = list()
        for x in range(len(all_boxes)):
            boxes = all_boxes[x]
            if (i2 == 0):
                # Laeuft einmal beim ersten frame
                n2 = 0
                while n2 < len(boxes):
                    ax = boxes[n2][0]
                    ay = boxes[n2][1]
                    n2 = n2 + 1
                i2 = i2 + 1
            for n in range(0,len(boxes)):
                if len(alteX) < len(boxes):
                    # erster run
                    alteX.append(boxes[n][0])
                    alteY.append(boxes[n][1])
                else:
                    # zweiter und folgende runs
                    dx = boxes[n][0] - alteX[n]
                    dy = boxes[n][1] - alteY[n]
                    alteX[n] = boxes[n][0]
                    alteY[n] = boxes[n][1]
                    dxy = math.sqrt(dx**2 + dy**2)
                    dxylist.append(int(dxy))
                    # *100
        dxylist.pop(0)
        dxylist.sort()

    def count_velocity(self):
        """
        Funktion die Geschwindigkeiten von den Pucks zählt.
        """
        anzahl = 0
        anzahlliste = list()
        anzahlliste.append(0)
        var1 = 0
        #position = 0
        global anzahllistedic 
        anzahllistedic= dict()
        for position in range(0,(len(dxylist) - 2)):
            if(dxylist[position] == var1):
                anzahl = anzahl + 1
            else:
                anzahllistedic[int(var1)] = int(anzahl)
                var1 = dxylist[position + 1]
                anzahlliste.append(0)
                if(dxylist[position] == var1):
                    anzahl = 1
                else:
                    anzahl = 0
        anzahllistedic[int(var1)] = int(anzahl)
        zaehleranzahl = np.arange(len(anzahlliste))

    def func(self,x, a, b, c):
        """
        Funktion welche für den Fit Befehl benutzt wird.
        """
        return a * x * np.exp(-b * x * x) + c

    def fit(self):
        """
        Berechnet den Fit auf die Geschwindigkeitsdaten.
        """
        # wieoft die v vorkommen
        self.aldvalue = list(anzahllistedic.values()) 
        # vorkommenden v
        self.aldkeys = list(anzahllistedic.keys())
        i3 = 0
        # Fitt Funktion:
        self.parameter, covariance_matrix = curve_fit(self.func, self.aldkeys, 
            self.aldvalue)
        #print(type(self.parameter))
        # Schritte in denen ich den Fitt ausgeben will:
        self.x = np.linspace(min(self.aldkeys), max(self.aldkeys), 1000)

    def plot_and_show(self):
        """
        Funktion zum anzeigen und berechnen der Plots
        """
        plt.plot(self.aldkeys, self.aldvalue, "rx")
        plt.plot(self.x, self.func(self.x, *self.parameter), 'b-')
        plt.show()
        
    def plot_and_save(self,path):
        """
        Speichert den bereits errechneten/geploteten graphen als Bild in 
        übergebenen Ort.
        """
        plt.plot(self.aldkeys, self.aldvalue, "rx")
        plt.plot(self.x, self.func(self.x, *self.parameter), 'b-')
        plt.savefig(path)