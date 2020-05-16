"""A set of tools accessible throughout the entire program.

Contains:
* data-continer classes (namely, the Condition class)
* gui classes that behave like tkinter widgets
"""

from tkinter import *
import pandas as pd
import numpy as np

print("loading case data...")
datapath = r"C:\Users\buffs\Documents\cases.xls"
cases = pd.read_html(datapath)[0]

ConditionDict = {}


class Condition:

    def __init__(self, name, isgrouped=False):
        self.name = name
        self.isgrouped = isgrouped
        self.series = cases[self.name].dropna()
        self.array = self.series.drop_duplicates().array

        if isgrouped:
            items = []
            for I in self.array:
                for i in I.split(" / "):
                    if i not in items:
                        items.append(i)
            self.array = np.array(items)

            falsearray = np.zeros((cases.index.size, self.array.size),
                                  dtype=bool)
            self.df = pd.DataFrame(falsearray, index=cases.index,
                                   columns=self.array)

            for case in self.series.index:
                I = self.series[case].split(" / ")
                for i in I:
                    self.df.at[case, i] = True

        ConditionDict[self.name] = self


print("processing case data...")
Species = Condition("Species")
Admit_Life_Stage = Condition("Admit. Life Stage")
Rescue_Jurisdiction = Condition("Rescue Jurisdiction")
Circumstances_of_Rescue = Condition("Circumstances of Rescue", isgrouped=True)
Injury = Condition("Injury", isgrouped=True)
Disposition = Condition("Disposition")
Disposition_Addit = Condition("Disposition Addit.")
Disposition_Jurisdiction = Condition("Disposition Jurisdiction")
To_Whom = Condition("To Whom")

defaultCondition = list(ConditionDict.keys())[0]

print("done\n")


class TkWidget:
    def grid(self, **kwargs):
        self.object.grid(**kwargs)
        return self

    def pack(self, **kwargs):
        self.object.pack(**kwargs)
        return self

    def pack_forget(self):
        self.object.pack_forget()

    def bind(self, *args):
        self.object.bind(*args)


class ConditionSelect(TkWidget):

    def update_display(self, name):
        self.set(name)
        self.tracefunc()
    def _update_display_command(self, name):
        return lambda: self.update_display(name)

    def get_condition(self):
        name = self.get()
        return ConditionDict[name]

    def set_tracefunc(self, tracefunc):
        self.tracefunc = tracefunc

    def __init__(self, frame):
        self._stringvar = StringVar()
        self.get = self._stringvar.get
        self.set = self._stringvar.set
        self.set(defaultCondition)
        def tracefunc(self): None

        self.object = Menubutton(
            frame, textvariable=self._stringvar, relief="raised")
        self._menu = Menu(self.object, tearoff=0)
        self.object["menu"] = self._menu

        for name in ConditionDict.keys():
            self._menu.add_command(
                label=name,
                command=self._update_display_command(name))


class Window(TkWidget):

    def get_selected(self):
        index = self.listbox.curselection()
        selected = []
        for i in index:
            selected.append(self.listbox.get(i))
        return selected


class VarWindow(Window):

    def build_box(self, condition):
        self.condition = condition
        varlist = self.condition.array
        self.listbox.delete(0, "end")
        for i in range(len(varlist)):
            self.listbox.insert(i, varlist[i])

    def filter(self, string):
        varlist = self.condition.array
        self.listbox.delete(0, "end")
        for var in varlist:
            if string.lower() in var.lower():
                self.listbox.insert(self.listbox.size(), var)

    def __init__(self, frame):
        self.object = Frame(frame)
        self._sbar = Scrollbar(self.object)
        self.listbox = Listbox(
            self.object, yscrollcommand=self._sbar.set,
            width=50, height=19, selectmode="extended")
        self.listbox.pack(side="left")
        self._sbar.pack(side="right", fill="y")
        self._sbar.config(command=self.listbox.yview)

        self.build_box(ConditionDict[defaultCondition])


class SelectedWindow(Window):

    def add(self, varlist):
        allvars = self.listbox.get(0, last="end")
        for var in varlist:
            if var not in allvars:
                self.listbox.insert(self.listbox.size(), var)

    def remove(self, *args):
        index = list(self.listbox.curselection())
        index.sort(reverse=True)
        for i in index:
            self.listbox.delete(i)

    def __init__(self, frame):
        self.object = Frame(frame)
        self.listbox = Listbox(self.object, width=50, height=19,
            selectmode="extended")
        self.listbox.pack()


class Filter(TkWidget):

    def get_filter(self):
        return self._filter.get()

    def add_trace(self, tracefunc):
        self._filter.trace_add("write", tracefunc)

    def __init__(self, frame):
        self.object = Frame(frame)
        self._label = Label(self.object, text="Filter: ").pack(side="left")
        self._filter = StringVar()
        self.entry = Entry(self.object,
            textvariable=self._filter).pack(side="right")


class VarSelector(TkWidget):

    def add(self, *args):
        selected = self._var_window.get_selected()
        addlist = []
        for i in selected:
            addlist.append((self._condition_selector.get(), i))
        self._selected_window.add(addlist)

    def _filter_trace(self, *args):
        string = self._filter.get_filter()
        self._var_window.filter(string)

    def _condition_trace(self):
        condition = self._condition_selector.get_condition()
        self._var_window.build_box(condition)

    def __init__(self, frame):
        self.object = Frame(frame)
        self._condition_selector = ConditionSelect(self.object)
        self._condition_selector.grid(row=0, column=0)
        self._condition_selector.set_tracefunc(self._condition_trace)
        self._var_window = VarWindow(self.object).grid(row=1, column=0)
        self._selected_window = SelectedWindow(self.object).grid(row=1, column=1)
        self._add_button = Button(
            self.object, text="Add Variable",
            command=self.add).grid(row=2, column=0)
        self._remove_button = Button(
            self.object, text="Remove Variable",
            command=self._selected_window.remove).grid(row=2, column=1)
        self._filter = Filter(self.object).grid(row=3, column=0)
        self._filter.add_trace(self._filter_trace)

        self._var_window.listbox.bind("<Return>", self.add)
        self._selected_window.listbox.bind("<BackSpace>",
                                         self._selected_window.remove)


if __name__ == "__main__":

    root = Tk()
    root.title("toolbox")

    var_selector = VarSelector(root).pack()

    root.mainloop()
