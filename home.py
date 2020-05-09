# Home Window

from toolbox import *

class Home(TkWidget):
    def __init__(self, frame):
        self.object = Frame(frame)
        self.label = Label(self.object, text="Home").pack()

if __name__ == "__main__":

    root = Tk()
    Home = Home(root).pack()
    root.mainloop()
