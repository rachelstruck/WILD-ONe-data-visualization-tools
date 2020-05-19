"""File Selection"""

from toolbox import *
from datatools import *

class File(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.label = Label(self, text="File")
        self.label.pack()
        self.entry = Entry(self)
        self.entry.pack()
        self.button = Button(text="GO", width=10, command=load_data(self.entry.get()))
        self.button.pack()

if __name__ == "__main__":

    root = Tk()
    File(root).pack()
    root.mainloop()
