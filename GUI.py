import Tkinter
from Tkinter import *
from tkFileDialog import askopenfilename
from ProcessCapturing import *
from multiprocessing import Pool
import ProcessCapturing
from ManualScan import *


_FINISH = False
pool = None

def browseTxt():
    Tk().withdraw()
    global filename
    filename = ""
    filename = askopenfilename()

def startThread():
    global pool
    pool = Pool(processes=1)
    p = pool.apply_async(scan, [])
    return p


def stopThread():
    ProcessCapturing._FINISH = True
    pool.terminate()
    pool.join()


def popupWindow():
    popup = Tk()
    popup.wm_title("GUI Error")
    popup.geometry("550x150+300+230")
    label = Label(popup, text="Error in input! Make sure to fill in date1 date2 and upload a file path!",font=("Helvetica", 12))
    label.pack(pady=10)
    b1 = Button(popup, text="Okay", command=popup.destroy)
    b1.pack(pady=5)


def manualScan():
    #Input Check First
    if startDate.get() is "" or endDatetime.get() is "" or filename is "":
        popupWindow()
    else:
        date1 = startDate.get()
        date2 = endDatetime.get()
        print date1
        print filename
        print date2
        manualScaning(filename, date1, date2)


gui = Tk()
gui.title("GUI")
gui.geometry("650x450+200+200")

Label(gui, text="Manual Process Scan",font=("Helvetica", 16)).grid(row=0, column=1)
Label(gui).grid(row=0, column=2)
Label(gui, text="Automatic Process Scan",font=("Helvetica", 16)).grid(row=5, column=1)



Label(gui, text="Start Datetime", font=("Helvetica", 12)).grid(row=1, column=1)
Label(gui, text="End Datetime", font=("Helvetica", 12)).grid(row=2, column=1)


startDate = Entry(gui)
startDate.grid(row=1, column=2)


endDatetime = Entry(gui)
endDatetime.grid(row=2, column=2)

txtUpload = Tkinter.Button(gui, text="Upload a file", width=20,command=browseTxt)
txtUpload.grid(row=3, column=2)

manualScanButton = Button(gui,text="Start Manual Scan", width=20,height=1, command=manualScan)
manualScanButton.grid(row=4, column=2)

capture = Tkinter.Button(gui, text="Start capturing", width=20, command=startThread)
capture.grid(row=6, column=1)

stopCapture = Tkinter.Button(gui, text="Stop capturing", width=20, command=stopThread)
stopCapture.grid(row=7, column=1)

gui.mainloop()

