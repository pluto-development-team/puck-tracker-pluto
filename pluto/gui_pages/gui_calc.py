import tkinter as tk
from tkinter import ttk  
        
class CalcPage(ttk.Frame):
    
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        self.grid_columnconfigure(1, weight=1)
        
        status = tk.Button(
            self,text="Start",width=10,height=2,command=controller.toggle)
        status.grid(row=0,column=0,padx=2,pady=2)
        
        progress = ttk.Progressbar(self,length=300,mode="determinate")
        progress.grid(row=0,column=1,columnspan=3,padx=2,pady=2,sticky="nsew")    
        
        stats = ttk.LabelFrame(self,text="Infos")
        stats.grid(row=1, column=0,columnspan=4,padx=2,pady=2)
        
        frame = ttk.Label(stats,text="Frames: ")
        frame.pack(expand=1)
        
        time = ttk.Label(stats,text="Zeit vergangen: ")
        time.pack(expand=1)
        
        eta = ttk.Label(stats,text="ETA: ")
        eta.pack(expand=1)
