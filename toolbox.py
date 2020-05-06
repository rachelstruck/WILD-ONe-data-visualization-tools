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
        self.series = cases[self.name]
        self.array = self.series.drop_duplicates().dropna().array

        if isgrouped:
            items = []
            for I in self.array:
                for i in I.split(" / "):
                    if i not in items:
                        items.append(i)
            self.array = items

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

    def bind(self, *args):
        self.object.bind(*args)

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

class Window(TkWidget):

    def getSelected(self):
        index = self.listbox.curselection()
        selected = []
        for i in index:
            selected.append(self.listbox.get(i))
        return selected

class VarWindow(Window):

    def buildBox(self, condition):
        self.condition = condition
        varlist = self.condition.array
        self.listbox.delete(0, 'end')
        for i in range(len(varlist)):
            self.listbox.insert(i, varlist[i])

    def filter(self, string):
        varlist = self.condition.array
        self.listbox.delete(0, 'end')
        for var in varlist:
            if string.lower() in var.lower():
                self.listbox.insert(self.listbox.size(), var)

    def __init__(self, frame):
        self.object = Frame(frame)
        self.sbar = Scrollbar(self.object)
        self.listbox = Listbox(self.object, yscrollcommand=self.sbar.set,
            width=50, height=19, selectmode='extended')
        self.listbox.pack(side='left')
        self.sbar.pack(side='right', fill='y')
        self.sbar.config(command=self.listbox.yview)

        self.buildBox( ConditionDict[defaultCondition] )

class SelectedWindow(Window):

    def add(self, varlist):
        allvars = self.listbox.get(0, last='end')
        for var in varlist:
            if var not in allvars:
                self.listbox.insert(self.listbox.size(), var)

    def remove(self, *args):
        index = list( self.listbox.curselection() )
        index.sort(reverse=True)
        for i in index:
            self.listbox.delete(i)

    def __init__(self, frame):
        self.object = Frame(frame)
        self.listbox = Listbox(self.object, width=50, height=19,
            selectmode='extended')
        self.listbox.pack()

class Filter(TkWidget):

    def getFilter(self):
        return self.filter.get()

    def addTrace(self, tracefunc):
        self.filter.trace_add("write", tracefunc)

    def __init__(self, frame):
        self.object = Frame(frame)
        self.label = Label(self.object, text='Filter: ').pack(side='left')
        self.filter = StringVar()
        self.entry = Entry(self.object,
            textvariable=self.filter).pack(side='right')

class VarSelector(TkWidget):

    def add(self, *args):
        selected = self.VarWindow.getSelected()
        self.SelectedWindow.add(selected)

    def filterTrace(self, *args):
        string = self.filter.getFilter()
        self.VarWindow.filter(string)

    def conditionTrace(self):
        condition = self.ConditionSelector.getCondition()
        self.VarWindow.buildBox(condition)

    def __init__(self, frame):
        self.object = Frame(frame)
        self.ConditionSelector = ConditionSelect(self.object).grid(row=0, column=0)
        self.ConditionSelector.setTracefunc(self.conditionTrace)
        self.VarWindow = VarWindow(self.object).grid(row=1, column=0)
        self.SelectedWindow = SelectedWindow(self.object).grid(row=1, column=1)
        self.addButton = Button(self.object, text="Add Variable",
            command=self.add).grid(row=2, column=0)
        self.removeButton = Button(self.object, text="Remove Variable",
            command=self.SelectedWindow.remove).grid(row=2, column=1)
        self.filter = Filter(self.object).grid(row=3, column=0)
        self.filter.addTrace(self.filterTrace)

        self.VarWindow.listbox.bind("<Return>", self.add)
        self.SelectedWindow.listbox.bind("<BackSpace>",
            self.SelectedWindow.remove)

if __name__ == '__main__':

    import tkinter as tk

    root = Tk()
    root.title("toolbox")

    VS = VarSelector(root).pack()

    root.mainloop()
