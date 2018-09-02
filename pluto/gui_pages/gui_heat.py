"""
Datei für Klasse welche die Heatmap Seite beinhaltet. Diese wiederum 
implementiert das calc Modul Heatmap() benutzt
"""

__authoer__ = "Claas Fillies, Jannis Jüppner, Friedrich Rieber"
__version__ = "1.0"

import tkinter as tk
from tkinter import ttk  
from gui_pages.calc_modules.heatmap import Heatmap
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg 

class HeatPage(ttk.Frame):
	
	heat = Heatmap() 
	all_boxes_backup = list()

	def __init__(self, parent, controller):
		"""
		Konstruktor der die Seite initialisiert und die noetigen Knoepfe
		erstellt.
		"""

		ttk.Frame.__init__(self,parent)
		label = tk.Label(self,text="Heatmap")
		label.pack()

		button_calc = tk.Button(
			self,
			text="Berechnen",
			width=10,
			height=2,
			command=controller.calc_heat)
		button_calc.pack(expand=1)
		
	def calculate(self,all_boxes):
		"""
		Haupt Rechen Funktion der Klasse welche die Rechnungs Funktion des
		Moduls auswählt [hier calculate_heatmap()]
		"""
		self.all_boxes_backup = all_boxes
		self.heat.calculate_heatmap(all_boxes)

		fig, self.ax = plt.subplots()

		im = self.ax.imshow(self.heat.matrix, cmap="gnuplot2_r",)
		self.ax.set_title(self.heat.titel)
		cbar = self.ax.figure.colorbar(im, ax=self.ax)
		cbar.ax.set_ylabel(self.heat.seitenlabel, rotation=-90,va="bottom")
		fig.tight_layout()
		
		self.canvas_plot(fig)


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