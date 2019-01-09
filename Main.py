import sys
import tkinter as tk
import ResaleFlat as rfp
import ResalePriceIndex as rpi
import CoolingMeasure as clm
import LineChartByTown as lct
import SpecificFlat as sff
import ResaleApplication as rac
import HDBdwelling as hdl
from PIL import ImageTk, Image

def ResalePriceIndex():
    rpi.genResalePriceIndex()
    print("Resale Flat Price index!")
def CoolingMeasure():
    clm.genCoolingMeasure()
    print("Cooling Measures!")
def LineChartByTown():
    lct.genLineChartByTown("2007", "2", "4-room")
    print("Resale Flat Price By Town!")
def ResaleFlat():
    rfp.genResaleFlatPriceGraph("2017", "01", "50", "4 ROOM", [])
    print("Resale Flat By Town!")
def SpecificFlat():
    sff.genSpecificFlat()
    print("Specific Resale Flat Price By Street!")
def ResaleApplication():
    rac.genResaleApplication()
    print("Resale Flat Volume By Flat Type!")
def HDBdwelling():
    hdl.genHDBdwelling()
    print("Resale Flat Ethnic Group By Flat Type!")
def ImportData():
    print("Import HDB Data in Contruction")
def About():
    print("Help Menu in Contruction")
    
#This creates the main window of an application
window = tk.Tk()
window.title("HDB Resale Flat")
window.geometry("900x540")
window.configure(background='grey')

path = "HDB.jpg"
#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img = ImageTk.PhotoImage(Image.open(path))

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
panel = tk.Label(window, image = img)

#The Pack geometry manager packs widgets in rows or columns.
panel.pack(side = "bottom", fill = "both", expand = "yes")

menu = tk.Menu(window)
window.config(menu=menu)
filemenu = tk.Menu(menu)
menu.add_cascade(label="Program    ", menu=filemenu)
filemenu.add_command(label="Resale Flat Price index", command=ResalePriceIndex)
filemenu.add_command(label="Cooling Measures", command=CoolingMeasure)
filemenu.add_command(label="Resale Flat Price By Town", command=LineChartByTown)
filemenu.add_separator()
filemenu.add_command(label="Resale Flat By Town", command=ResaleFlat)
filemenu.add_command(label="Specific Resale Flat Price By Street", command=SpecificFlat)
filemenu.add_separator()
filemenu.add_command(label="Resale Flat Volume By Flat Type", command=ResaleApplication)
filemenu.add_command(label="Resale Flat Ethnic Group By Flat Type", command=HDBdwelling)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)

helpmenu = tk.Menu(menu)
menu.add_cascade(label="Help    ", menu=helpmenu)
helpmenu.add_command(label="Import HDB Data", command=ImportData)
helpmenu.add_command(label="About...", command=About)

window.mainloop()