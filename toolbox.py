# A set of tools to more easily build frames.

from tkinter import *
import pandas as pd

print("loading case data...")
datapath = r"C:\Users\buffs\Documents\cases.xls"
cases = pd.read_html(datapath)[0]
print("done\n")

ConditionDict = {}

class Condition:

    def __init__(self, name, isgrouped=False):
        self.name = name
        self.isgrouped = isgrouped
        self.series = cases[self.name].drop_duplicates()
        self.array = self.series.dropna().array

        ConditionDict[self.name] = self

Species = Condition('Species')
Admit_Life_Stage = Condition('Admit. Life Stage')
Rescue_Jurisdiction = Condition('Rescue Jurisdiction')
Circumstances_of_Rescue = Condition('Circumstances of Rescue', isgrouped=True)
Injury = Condition('Injury', isgrouped=True)
Disposition = Condition('Disposition')
Disposition_Addit = Condition('Disposition Addit.')
Disposition_Jurisdiction = Condition('Disposition Jurisdiction')
To_Whom = Condition('To Whom')

defaultCondition = list( ConditionDict.keys() )[0]

class TkWidget:
    def grid(self, **kwargs):
        self.object.grid(**kwargs)
        return self

    def pack(self, **kwargs):
        self.object.pack(**kwargs)
        return self

class ConditionSelect(TkWidget):

    def UpdateDisplay(self, name):
        self.set(name)
        self.tracefunc()
    def UpdateDisplayCommand(self, name):
        return lambda: self.UpdateDisplay(name)

    def getCondition(self):
        name = self.get()
        return ConditionDict[name]

    def setTracefunc(self, tracefunc):
        self.tracefunc = tracefunc

    def __init__(self, frame):
        self.stringvar = StringVar()
        self.get = self.stringvar.get
        self.set = self.stringvar.set
        self.set(defaultCondition)
        self.tracefunc = lambda: None

        self.object = Menubutton(
            frame, textvariable=self.stringvar, relief='raised')
        self.menu = Menu(self.object, tearoff=0)
        self.object['menu'] = self.menu

        for name in ConditionDict.keys():
            self.menu.add_command(label=name,
                command=self.UpdateDisplayCommand(name))

class VarWindow(TkWidget):

    def buildBox(self, condition):
        self.condition = condition
        varlist = self.condition.array
        self.object.delete(0, 'end')
        for i in range(len(varlist)):
            self.object.insert(i, varlist[i])

    def filter(self, string):
        varlist = self.condition.array
        self.object.delete(0, 'end')
        for var in varlist:
            if string in var:
                self.object.insert(self.object.size(), var)

    def getSelected(self):
        index = self.object.curselection()
        selected = []
        for i in index:
            selected.append(self.object.get(i))
        return selected

    def __init__(self, frame):
        self.sbar = Scrollbar(frame)
        self.sbar.pack(side='right', fill='y')
        self.object = Listbox(frame, yscrollcommand=self.sbar.set,
            width=50, height=19, selectmode='extended')
        self.sbar.config(command=self.object.yview)

        self.buildBox( ConditionDict[defaultCondition] )

class SelectedWindow(TkWidget):

    def add(self, varlist):
        for var in varlist:
            self.object.insert(self.object.size(), var)

    def remove(self):
        index = list( self.object.curselection() )
        index.sort(reverse=True)
        for i in index:
            self.object.delete(i)

    def __init__(self, frame):
        self.object = Listbox(frame, width=50, height=19,
            selectmode='extended')

class VarSelector(TkWidget):

    def __init__(self, frame):
        self.frame = Frame(frame)
        self.ConditionSelector = ConditionSelect().grid(row=0, column=0)
        self.VarWindow = VarWindow().grid(row=1, column=0)
        self.SelectedWindow = SelectedWindow().grid(row=1, column=1)

if __name__ == '__main__':

    import tkinter as tk

    root = Tk()

    box = VarWindow(root)


    b = ConditionSelect(root)
    def f():
        box.buildBox(b.getCondition())
    b.setTracefunc(lambda: box.buildBox(b.getCondition()))
    b.pack()

    p = Button(
        root, text="print selection",
        command=lambda: selected.add( box.getSelected() )
        )
    p.pack()

    box.pack()

    selected = SelectedWindow(root).pack()
    delButton = Button(
        root, text="delete", command=lambda: selected.remove()
        ).pack()

    root.mainloop()
