# Main window of the Application

import tkinter as tk
from toolbox import ConditionSelect

# Creates main window
root = tk.Tk()
root.title('Hello World')

# Create button panel at the left of the window
ButtonFrame = tk.Frame(root)
tk.Button(ButtonFrame, text='Home', width=10).pack()
tk.Button(ButtonFrame, text='Spreadsheet', width=10).pack()
tk.Button(ButtonFrame, text='Time Plot', width=10).pack()
ButtonFrame.grid(column=0, row=0)

# Creates content at the right
ContentFrame = tk.Frame(root)
tk.Label(ContentFrame, text='here is some text you can see').pack()
ContentFrame.grid(column=1, row=0)

root.mainloop()
