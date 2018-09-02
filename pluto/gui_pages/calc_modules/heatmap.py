import numpy as np
import matplotlib.pyplot as plt
import pickle


__author__ = "Jannis Jüppner, Claas Filies"
__version__ = "1.0"


class Heatmap:
	
	x_bild = 1920                       #Auflösung der Kamera -> Anzahl an Pixeln im Bild
	y_bild = 1080                       #demzufolge Minimalgröße des Gitters
	kasten_groesse = 100                #Seitenlänge der Kästen der Heatmaps in Pixeln 
			
	matrix = []                         #leere Hilfsliste, in der die Daten von all_boxes in Daten für die Heatmap 
										#umgewandelt werden.

	m = "x"
	a = "r"
	b = "a"
	c = 0
	titel = ""
	seitenlabel = ""

	def  calculate_heatmap(self,all_boxes):
		"""
		"""
		#horizontale Anzahl der Kästen in Heatmap    
		breite = int(self.x_bild/self.kasten_groesse)
		#vertikale Anzahl der Kästen in Heatmap  
		hoehe = int(self.y_bild/self.kasten_groesse) 

		# i = y, j = x
		for i in range(0,hoehe):
			# auf gesamter Höhe der Heatmapmatrix wird für jede Zeile
			# eine neue Liste erstellt.
			self.matrix.append([])  
			for j in range(0,breite):
				# auf gesamter Breite der Heatmapmatrix wird für jede 
				# Spalte eine 0 eingefügt.
				self.matrix[i].append(0) 

		# i = y, j = x
		# alle Zeilen von all_boxes werden durchiteriert; Zeilen = Frames
		for i in range(len(all_boxes)):
			# wenn alle Pucks angezeigt werden sollen, 
			# interessieren auch die Spalten (ein Puck eine Spalte)
			if self.b == "a": 
				#alle Spalten von all_boxes werden durchiteriert
				for j in range(len(all_boxes[i])): 
					#wenn Punkt
					self.matrix[int(all_boxes[i][j][1]/self.kasten_groesse)][int(all_boxes[i][j][0]/self.kasten_groesse)] += 1 
					#in all_boxes sich im Kasten für Matrix befindet, bekommt die 0 im Matrixfeld ein +1
			if self.b == "e":
				#statt alle Spalten durchzugehen wird nur die c'te Spalte betrachtet für den c'ten Puck
				j = self.c 
				self.matrix[int(all_boxes[i][j][1]/self.kasten_groesse)][int(all_boxes[i][j][0]/self.kasten_groesse)] += 1 #wenn Punkt in
				#all_boxes (Spalte des Pucks) sich im Kasten für Matrix befindet, bekommt die 0 im Matrixfeld ein +1
		
		#c wird zurück auf 1 bis 18 gewechselt für Beschriftung der Heatmap
		self.c += 1         

		if self.a == "r":        #Umwandlung von absoluten zu relativen Werten
			for i in range(hoehe):  #Matrixeinträge sind absolute Anzahl an Frames, in denen ein Puck gefundet wurde
				for j in range(breite): #Umwandlung indem durch die Anzahl an Frames geteilt wird (Länge all_boxes = Frames)
					self.matrix[i][j] /= len(all_boxes) #(Pucks*Frames)/(Zeit*Frames) = Pucks/Zeit
					self.matrix[i][j] *= 100 #relative Werten von 0 bis 1 werden in Prozent umgewandelt
		#c wird zurück auf 1 bis 18 gewechselt für Beschriftung der Heatmap
		
		if self.a == "a": 
			#Änderungen vorgenommen werden 
			None     

		if self.a == "a":
			y = "absolute"
		if self.a == "r":
			y = "relative"
			
		if self.a == "a" and self.m == "x":
			self.seitenlabel = "Frames mit Aufenthalt x"
		if self.a == "a" and self.m == "v":
			self.seitenlabel = "Frames mit Geschwindigkeit v"
		if self.a == "r" and self.m == "x":
			self.seitenlabel = "% der Zeit mit Aufenthalt x"
		if self.a == "r" and self.m == "v":
			self.seitenlabel = "% der Zeit mit Geschwindigkeit v"

		if self.m == "x":
			n = "Aufenthaltswahrscheinlichkeit"
		if self.m == "v":
			n = "Geschwindigkeitsverteilung"

		if self.b == "a":
			self.titel = "{} {} aller Pucks".format(y,n)
		if self.b == "e":
			self.titel = "{} {} von Puck {}".format(y,n,self.c)

