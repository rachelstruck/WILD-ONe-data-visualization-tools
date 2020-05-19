"""File Selection"""

from toolbox import *
from datatools import *

class File(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.label = Label(self, text="File")
        self.label.pack()
        self.entry = Entry(self)
        self.entry.pack()
        self.button = Button(text="GO", width=10,
                             command=lambda: load_data(self.entry.get()))
        # Here, we have to use a lambda function because the command argument
        # only accepts function type arguments. If you call the function
        # you are trying to set command to, then you are setting command
        # to the output of the function, not the function itself. Using
        # lambda, we can create a function that, when called, does what
        # you want the button to do, which is exactly what we want command
        # to be.
        self.button.pack()

if __name__ == "__main__":

    root = Tk()
    File(root).pack()
    root.mainloop()
