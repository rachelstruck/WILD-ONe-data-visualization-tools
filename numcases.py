# Number of Cases Applet

from toolbox import *

class NumOfCases(TkWidget):
    def __init__(self, frame):
        self.object = Frame(frame)
        self.label = Label(self.object, text="Number of Cases").pack()

if __name__ == "__main__":

    root = Tk()
    NumOfCases = NumOfCases(root).pack()
    root.mainloop()
