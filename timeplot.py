"""Time Plot Applet"""

from toolbox import *

class TimePlot(TkWidget):
    def __init__(self, frame):
        self.object = Frame(frame)
        self.label = Label(self.object, text="Time Plot").pack()

if __name__ == "__main__":

    root = Tk()
    time_plot = TimePlot(root).pack()
    root.mainloop()
