"""Pie Chart Applet"""

from toolboxreborn import *

class PieChart(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.label = Label(self, text="Pie Chart")
        self.label.pack()

if __name__ == "__main__":

    root = Tk()
    PieChart(root).pack()
    root.mainloop()
