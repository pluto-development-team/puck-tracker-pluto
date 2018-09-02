import tkinter as tk
from tkinter import ttk  
        
class InputPage(ttk.Frame):
    
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        label_video = ttk.Label(self,text="Video wählen:",width=18)
        label_video.grid(row=0,column=0,padx=2,pady=2)
        
        button_video = tk.Button(
            self,text="Video öffnen",width=18,command=controller.openVideo)
        button_video.grid(row=0,column=1,padx=2,pady=2)
        
        label_cascade = ttk.Label(self,text="Kaskade wählen:",width=18)
        label_cascade.grid(row=2,column=0,padx=2,pady=2)
        
        button_cascade = tk.Button(
            self,text="Kaskade öffnen",width=18,command=controller.openCascade)
        button_cascade.grid(row=2,column=1,padx=2,pady=2)
