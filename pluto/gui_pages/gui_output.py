import tkinter as tk
from tkinter import ttk          
        
class OutputPage(ttk.Frame):
    
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        table_export = tk.Button(
            self,
            text="Positionsdaten exportieren",
            width=20,command=controller.outputTable)
        table_export.pack(expand=1)
        
 
