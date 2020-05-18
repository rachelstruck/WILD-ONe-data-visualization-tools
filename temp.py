import tkinter as tk

class HelloButton(tk.Button):

    def say_hi(self):
        print("hi!")

    def __init__(self, parent):
        tk.Button.__init__(self, parent, text="Hello", command=self.say_hi)
        self.pack()

if __name__ == "__main__":

    root = tk.Tk()
    HelloButton(root).pack()
    root.mainloop()
