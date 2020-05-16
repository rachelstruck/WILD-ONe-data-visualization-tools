# Spreadsheet Applet

from toolbox import *

class Spreadsheet(TkWidget):
    def __init__(self, frame):
        self.object = Frame(frame)
        self.label = Label(self.object, text="Spreadsheet").pack()

if __name__ == "__main__":

    root = Tk()
    spreadsheet = Spreadsheet(root).pack()
    root.mainloop()
