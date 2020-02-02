# Main window of the Application

import tkinter as tk

root = tk.Tk()

ButtonFrame = tk.Frame(root).grid(column=0, row=0)
tk.Button(ButtonFrame, text='Here1').grid(column=0, row=0)



ContentFrame = tk.Frame(root).grid(column=1, row=0)

tk.Label(root, text='here is some text you can see').grid(column=0, row=1, columnspan=2)

root.mainloop()
