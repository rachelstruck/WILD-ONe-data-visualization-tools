# Pie Chart Applet

from toolbox import *

class PieChart(TkWidget):
    def __init__(self, frame):
        self.object = Frame(frame)
        self.label = Label(self.object, text="Pie Chart").pack()

if __name__ == "__main__":

    root = Tk()
    pie_chart = PieChart(root).pack()
    root.mainloop()
