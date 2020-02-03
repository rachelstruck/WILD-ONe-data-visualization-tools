# Main window of the Application

from tkinter import *

# Creates main window
root = Tk()
root.title('Testing Window')

#creates the number counter
n = 0

def counterAdd():
    global n
    n = n + 1
    number = Label(root, text=n, fg='green', font=('arial',24)).grid(row=3, column=0, columnspan=2)
def counterSub():
    global n
    n = n - 1
    number = Label(root, text=n, fg='green', font=('arial',24)).grid(row=3, column=0, columnspan=2)

#creates widgets
#header
header = Label(root, text='Welcome to the Test Branch', font=('arial', 28), padx=10)
header.grid(row=0, column=0, columnspan=2)
#info
info = Label(root, text='Here in the testing branch, we are experimenting with new\nand exciting features to add to our data visualization\ntool to give user a more simple and enjoyable experience,\n feel free to explore!', font=('arial', 14), padx=20, pady=10).grid(row=1, column=0, columnspan=2)
#buttons
add = Button(root, text='add', width=15, border=0.7, command=counterAdd).grid(row=2, column=0)
remove = Button(root, text='remove', width=15, border=0.7, command=counterSub).grid(row=2, column=1)
#number


#runs window
root.mainloop()
