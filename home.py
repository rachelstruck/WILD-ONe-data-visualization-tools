"""Home Window"""

from toolboxreborn import *

class Home(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.label = Label(self, text="Home")
        self.label.pack()

if __name__ == "__main__":

    root = Tk()
    Home(root).pack()
    root.mainloop()
