"""Main window of the Application"""

from tkinter import *
from toolbox import *

from numcases import NumOfCases
from home import Home
from spreadsheet import Spreadsheet
from timeplot import TimePlot
from piechart import PieChart


def switch_window(win):
    global current_window
    current_window.pack_forget()
    current_window = win
    current_window.pack()


# Creates main window
root = Tk()
root.title("WILD-ONe Data Visualization Tools")

# Create button panel at the left of the window
button_width = 13
button_frame = Frame(root)
Button(button_frame, text="Home", width=button_width,
    command=lambda: switch_window(home)).pack()
Button(button_frame, text="Number of Cases", width=button_width,
    command=lambda: switch_window(num_of_cases)).pack()
Button(button_frame, text="Spreadsheet", width=button_width,
    command=lambda: switch_window(spreadsheet)).pack()
Button(button_frame, text="Time Plot", width=button_width,
    command=lambda: switch_window(time_plot)).pack()
Button(button_frame, text="Pie Chart", width=button_width,
    command=lambda: switch_window(pie_chart)).pack()
button_frame.grid(column=0, row=0, sticky="NW")

# Creates content at the right
content_frame = Frame(root)
content_frame.grid(column=1, row=0)

main_window_list = []

home = Home(content_frame)
main_window_list.append(home)

num_of_cases = NumOfCases(content_frame)
main_window_list.append(num_of_cases)

spreadsheet = Spreadsheet(content_frame)
main_window_list.append(spreadsheet)

time_plot = TimePlot(content_frame)
main_window_list.append(time_plot)

pie_chart = PieChart(content_frame)
main_window_list.append(pie_chart)

current_window = home
current_window.pack()

root.mainloop()
