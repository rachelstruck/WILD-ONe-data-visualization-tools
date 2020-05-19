"""File Selection"""

from toolbox import *

class File(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.label = Label(self, text="File")
        self.label.pack()

if __name__ == "__main__":

    root = Tk()
    File(root).pack()
    root.mainloop()
