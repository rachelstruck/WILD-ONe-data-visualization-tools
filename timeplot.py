"""Time Plot Applet"""

from toolbox import *

class TimePlot(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.label = Label(self, text="Time Plot")
        self.label.pack()

if __name__ == "__main__":

    root = Tk()
    TimePlot(root).pack()
    root.mainloop()
