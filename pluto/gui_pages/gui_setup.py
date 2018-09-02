import tkinter as tk
from tkinter import ttk  
        
class SetupPage(ttk.Frame):
    
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        button_manual = tk.Button(
            self,text="manuelle Auswahl",
            width=20,command=controller.manualDetect)
        button_manual.grid(row=0,column=0)
        
        button_auto = tk.Button(
            self,text="automatische Auswahl",
            width=20,command=controller.autoDetect)
        button_auto.grid(row=0,column=1)
