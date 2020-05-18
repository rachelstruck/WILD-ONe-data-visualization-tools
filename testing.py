# Main window of the Application


from tkinter import *
from toolbox import *

#asldkfjbsn g;obo re[ab b vqwj,idsgcjlomewb tv; j twv4mb .vcfbp,j [npe]]
# Creates main window
root = Tk()
root.title('Testing Window')


# Creates the number counter
n = IntVar()
n.set(0)
number = Label(root, textvariable=n, fg='green', font=('arial',24))
number.grid(row=3, column=0, columnspan=2)

def counterAdd():
    n.set( n.get() + 1 )
def counterSub():
    n.set( n.get() - 1 )


# Creates widgets
# Header
header = Label(
    root, text='Welcome to the Test Branch', font=('arial', 28), padx=10)
header.grid(row=0, column=0, columnspan=2)

# Info
info = Label(root,
    text=   'Here in the testing branch, we are experimenting with new\n'
        +   'and exciting features to add to our data visualization\n'
        +   'tool to give user a more simple and enjoyable experience,\n'
        +   'feel free to explore!',
    font=('arial', 14), padx=20, pady=10)
info.grid(row=1, column=0, columnspan=2)

# Buttons
add = Button(root, text='add', width=15, border=0.7, command=counterAdd)
add.grid(row=2, column=0)
remove = Button(root, text='remove', width=15, border=0.7, command=counterSub)
remove.grid(row=2, column=1)

# Toolbox test
ConditionSelect(root).grid(row=3, column=0)

# Runs window
root.mainloop()
