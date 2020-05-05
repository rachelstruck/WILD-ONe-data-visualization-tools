# Main window of the Application

from tkinter import *
from toolbox import ConditionSelect

# Creates main window
root = Tk()
root.title('Hello World')

# Create button panel at the left of the window
ButtonFrame = Frame(root)
Button(ButtonFrame, text='Home', width=10).pack()
Button(ButtonFrame, text='Spreadsheet', width=10).pack()
Button(ButtonFrame, text='Time Plot', width=10).pack()
Button(ButtonFrame, text='Pie Chart', width=10).pack()
ButtonFrame.grid(column=0, row=0)

# Creates content at the right
ContentFrame = Frame(root)
Label(ContentFrame, text='here is some text you can see').pack()
ContentFrame.grid(column=1, row=0)

root.mainloop()
