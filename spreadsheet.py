"""Spreadsheet Applet"""

from toolboxreborn import *

class Spreadsheet(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.label = Label(self, text="Spreadsheet")
        self.label.pack()

if __name__ == "__main__":

    root = Tk()
    Spreadsheet(root).pack()
    root.mainloop()
