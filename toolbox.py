# A set of tools to more easily build frames.

from tkinter import *

ConditionDict = {}

class Condition:

    def __init__(self, name, isgrouped=False):
        self.name = name
        self.isgrouped = isgrouped
        #self.series = cases[self.name]

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

class ConditionSelect:

    def UpdateDisplay(self, name):
        return lambda: self.set(name)

    def grid(self, **kwargs):
        self.object.grid(**kwargs)
        return self

    def pack(self, **kwargs):
        self.object.pack(**kwargs)
        return self

    def __init__(self, frame):
        self.stringvar = StringVar()
        self.get = self.stringvar.get
        self.set = self.stringvar.set
        self.set(list(ConditionDict.keys())[0])

        def getCondition(self):
            name = self.get()
            return ConditionDict[name]

        self.object = Menubutton(
            frame, textvariable=self.stringvar, relief='raised')
        self.menu = Menu(self.object, tearoff=0)
        self.object['menu'] = self.menu

        for name in ConditionDict.keys():
            self.menu.add_command(label=name, command=self.UpdateDisplay(name))

if __name__ == '__main__':

    import tkinter as tk

    root = Tk()

    b = ConditionSelect(root)
    b.pack()

    root.mainloop()
