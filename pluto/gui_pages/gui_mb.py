"""
Datei für die Maxwell-Boltzmann Seite welche wiederrum das calc Mdoul 
MbFit() aufruft
"""
__authoer__ = "Friedrich Rieber"
__version__ = "1.0"

import tkinter as tk
from tkinter import ttk  
# canvas zeug
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg 
# Befehl zum Einstellen des Backends von Matplotlib
matplotlib.use('TkAgg')
# Für Beispiel
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from gui_pages.calc_modules.mb_fit import MbFit

# temporary import solange der Tracker keine Positionsdaten übergibt
import pickle

class MBPage(ttk.Frame):
	
	def __init__(self, parent, controller):

		ttk.Frame.__init__(self,parent)
		label = tk.Label(self,text="Maxwell-Boltzmann-Verteilung")
		label.pack()

		calc_button = tk.Button(
            self,
            text="Berechnen",
            width=10,
            height=2,
            command=controller.calc_mb)
		calc_button.pack(expand=1)

	def calculate(self,all_boxes):
		"""
		Berechnet die maxwell Boltzmann Verteilung aus übergebenen
		Daten und zeigt sie im GUI an
		"""

		fit = MbFit()
		fit.load_puck_data(all_boxes)
		fit.calc_and_fit()

		figure, self.plot_all = plt.subplots()
		self.plot_all.plot(fit.aldkeys,fit.aldvalue, "rx")
		self.plot_all.plot(fit.x,fit.func(fit.x,*fit.parameter),'b-')
		
		self.canvas_plot(figure)
	
	def canvas_plot(self,figure):
		"""
		Getrennte Funktion zum zeigen des Plots imk Gui. Die "Figure"
		wird übergeben, die einzelnen Elemente sind Klassen global.

		Eigene Funktion damit "gui_heat" und "gui_mb" gleich sind
		"""
		canvas = FigureCanvasTkAgg(figure, master = self)
		canvas.draw()
		canvas.get_tk_widget().pack()
		toolbar = NavigationToolbar2TkAgg(canvas, self)
		toolbar.update()

		canvas.get_tk_widget().pack()