# Main window of the Application

from tkinter import *
from toolbox import *

from numcases import NumOfCases
from home import Home
from spreadsheet import Spreadsheet
from timeplot import TimePlot
from piechart import PieChart


def SwitchWindow(win):
    global CurrentWindow
    CurrentWindow.pack_forget()
    CurrentWindow = win
    CurrentWindow.pack()


# Creates main window
root = Tk()
root.title('WILD-ONe Data Visualization Tools')


# Create button panel at the left of the window
button_width = 13
ButtonFrame = Frame(root)
Button(ButtonFrame, text='Home', width=button_width,
    command=lambda: SwitchWindow(Home)).pack()
Button(ButtonFrame, text='Number of Cases', width=button_width,
    command=lambda: SwitchWindow(NumOfCases)).pack()
Button(ButtonFrame, text='Spreadsheet', width=button_width,
    command=lambda: SwitchWindow(Spreadsheet)).pack()
Button(ButtonFrame, text='Time Plot', width=button_width,
    command=lambda: SwitchWindow(TimePlot)).pack()
Button(ButtonFrame, text='Pie Chart', width=button_width,
    command=lambda: SwitchWindow(PieChart)).pack()
ButtonFrame.grid(column=0, row=0)


# Creates content at the right
ContentFrame = Frame(root)
ContentFrame.grid(column=1, row=0)

MainWindowList = []

Home = Home(ContentFrame)
MainWindowList.append(Home)

NumOfCases = NumOfCases(ContentFrame)
MainWindowList.append(NumOfCases)

Spreadsheet = Spreadsheet(ContentFrame)
MainWindowList.append(Spreadsheet)

TimePlot = TimePlot(ContentFrame)
MainWindowList.append(TimePlot)

PieChart = PieChart(ContentFrame)
MainWindowList.append(PieChart)

CurrentWindow = Home
CurrentWindow.pack()

root.mainloop()
