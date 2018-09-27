import sys
import inspect
import copy
import numpy as np
import cv2
import matplotlib.pyplot as plt

#Gui / Tkinter importe
import tkinter as tk
from tkinter import ttk
from PIL import Image#, ImageTk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter.messagebox import showerror

from gui_pages.gui_calc import CalcPage
from gui_pages.gui_heat import HeatPage
from gui_pages.gui_input import InputPage
from gui_pages.gui_landing import LandingPage
from gui_pages.gui_mb import MBPage
from gui_pages.gui_output import OutputPage
from gui_pages.gui_setup import SetupPage

#Tracker und datenklasse
from datenklasse import *
import tracker

class mainApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        print(self)
        
        self.datacontainer = DataFrame()
        # ~ self.tracker = 
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self,"Mathesis Tracking")
        tk.Tk.geometry(self,"650x400")
        

        notebook = ttk.Notebook(self)
        notebook.pack(side="top", fill="both", expand=True)
        
        pages = [
                LandingPage,
                InputPage,
                SetupPage,
                CalcPage,
                HeatPage,
                MBPage,
                OutputPage
                ]
                
        self.reference = []
        
        for f in pages:
            page = f(notebook,self)
            self.reference.append(page)
            notebook.add(page, text=f.__name__[:-4])
        
        
    def openVideo(self):
        self.video_path = askopenfilename(
            filetypes=(("mp4-Datei", "*.mp4"),("All Files","*.*")))
            
        print(self.video_path)
            
    def openCascade(self):
        self.cascade_path = askopenfilename(
            filetypes=(("xml-Datei", "*.xml"),("All Files","*.*")))
            
        print(self.cascade_path)
    
    def autoDetect(self):
        sucess, maxframes, previewpic, numberofboxes, w, h = tracker.setup(
            self.video_path,self.cascade_path,True,None,False,"result")
        print(sucess,maxframes)
        
        self.maxframes = maxframes
        self.timepassed = 0

        for i in range(numberofboxes):
            self.datacontainer.addPuck(Puck())
            
        #Previewbild
        b,g,r = cv2.split(previewpic)
        img = cv2.merge((r,g,b))
        img = Image.fromarray(img)
        imgtk = tk.PhotoImage(img)
        
        # ~ self.reference[2].winfo_children()[2].configure("image")[-1] = imgtk
        # ~ self.reference[2].winfo_children()[2].image = imgtk
                
    def manualDetect(self):
        pass
        
    def outputTable(self):
        print("Hallo")
        save_path = asksaveasfile(defaultextension=".csv")
        print(save_path)
        self.datacontainer.save(save_path)
        
    def toggle(self):
        button = self.reference[3].winfo_children()[0]
        if button.config("text")[-1] == 'Start':
            button.config(text="Pause",relief="sunken")
            self.task()
        else:
            button.config(text="Start",relief="raised")
        
    def task(self):
        if self.reference[3].winfo_children()[0].config("text")[-1] == "Pause":
            #Tracking Loop
            
            state, self.frameCount, boxes, time, displayFrame = tracker.run()
            
            if state:
            
                self.timepassed += time
                
                #Datenübergabe an die Datenstruktur
                data = [self.frameCount]
                counter = 0
                for k in boxes:
                    n = (counter,k)
                    data.append(n)
                    counter += 1
                self.datacontainer.update(data)
                
                #Update der Ansicht
                self.after(0,self.update_view)
                
            else:
                tracker.cleanupTracker()
                self.reference[3].winfo_children()[0].configure(state="disabled")
            
    def update_view(self):
        showpage = self.reference[3].winfo_children()
        showpage[1]["maximum"] = self.maxframes
        showpage[1]["value"] = self.frameCount
        
        labels = showpage[2].winfo_children()
        labels[0].configure(
            text = "Frames: " + 
            str(int(self.frameCount)) + "/" + str(int(self.maxframes)))
        labels[1].configure(
            text = "Zeit vergangen: " + 
            self.timeconvert(self.timepassed))
        labels[2].configure(
            text = "ETA: " + 
            self.timeconvert((self.maxframes-self.frameCount) * self.timepassed/self.frameCount))
        
        self.update()
        self.after(0,self.task)
            
    def timeconvert(self,mil):
        mil = int(mil)
        second = int((mil/1000)%60)
        minute = int((mil/(1000*60))%60)
        hour = int((mil/(1000*60*60))%60)
        return ("0" if hour < 10 else "") + str(hour) + ":" + ("0" if minute < 10 else "") + str(minute) + ":" + ("0" if second < 10 else "") + str(second)
        
    def close_plot(self):
        plt.close()
        
    def calc_mb(self):
        if (len(sys.argv) > 1 and sys.argv[1] == "manuel_pos"):
            # debug option for testing
            import pickle 
            f = open("18_pucks_data.pkl","rb")
            all_boxes = pickle.load(f)
            print(all_boxes) 
            self.reference[5].calculate(all_boxes)
        else:
            print(self.datacontainer.data_boltzmann())
            self.reference[5].calculate(self.datacontainer.data_boltzmann())
        
    def calc_heat(self):
        self.reference[4].calculate(self.datacontainer.data_boltzmann())
        
        
            
if __name__ == "__main__":
    app = mainApp()
    app.mainloop()
