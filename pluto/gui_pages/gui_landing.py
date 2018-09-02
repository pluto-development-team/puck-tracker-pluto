import tkinter as tk
from tkinter import ttk

class LandingPage(ttk.Frame):
    
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        instruction_text = "Kurzanleitung:\n"\
            "\n"\
            "1. Video- und Kaskadendatei laden\n"\
            "2. Pucks detektieren\n3. Programm rechnen lassen\n"\
            "4. gewünschte Daten anzeigen / exportieren"
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        image = tk.PhotoImage(file="mintgruen_logo.gif")
        self.label = tk.Label(self, image=image)
        self.label.img = image
        #label.pack()
        self.label.grid(row=0,column=0)
        
        instruct = tk.Text(self)
        instruct.grid(row=1,column=0)
        instruct.insert('1.0', instruction_text)
        instruct.configure(state="disabled")

