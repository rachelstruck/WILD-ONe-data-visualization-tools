"""A set of tools accessible throughout the entire program.

Contains:
* data-continer class (the Condition class)
* gui classes that behave like tkinter widgets
    - TkWidget -- parent class of all tk-like classes
    - ConditionSelect -- menu button for selecting a condition object
    - Window -- parent class of listbox-like classes
    - VarWindow -- listbox to select items from a particular condition
    - SelectedWindow -- display selected items
    - Filter -- simple entry bar for entering filter strings
    - VarSelector -- gui to select any item from any condition
"""

from tkinter import *
import pandas as pd
import numpy as np

condition_tup = (
"Species", "Admit. Life Stage", "Rescue Jurisdiction",
"Circumstances of Rescue", "Injury", "Disposition", "Disposition Addit.",
"Disposition Jurisdiction", "To Whom"
)
toy_data = np.repeat("None", len(condition_tup)).reshape(1, 9)
# Toy data to make the program run when real data is not loaded

print("loading case data...")
datapath = r"not a valid path"
try:
    cases = pd.read_html(datapath)[0]
except ValueError:
    print("data not found, loading toy data...")
    cases = pd.DataFrame(toy_data, columns=condition_tup)


ConditionDict = {}
# Retrieve a condition object from its string name


class Condition:
    """Store the case data of a specific data heading.

    name -- the string name of the data header.
    isgrouped -- whether each case entry has multiple values separated by " / ".
    series -- the corresponding series in cases with null values removed.
    array -- the series as a array-like object with duplicates removed.
    """

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
    """Mimic the behavior of Tk widgets.

    All methods have the same behavior as their tkinter counterparts.
    """

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
    """Create a menu button to select a particular condition.

    Arguments:
    frame -- the tkinter parent window

    Public Methods: get, set, update_display, get_condition, set_tracefunc.
    get and set extend the get and set methods on the displayed string variable.

    Public Attributes:
    object -- the button object itself
    """

    def update_display(self, name):
        """Set the name that the button displays and call the trace function.

        Arguments:
        name -- the string to be displayed by the button
        """
        self.set(name)
        self.tracefunc()
    def _update_display_command(self, name):
        return lambda: self.update_display(name)

    def get_condition(self):
        """Return the condition object currently displayed."""
        name = self.get()
        return ConditionDict[name]

    def set_tracefunc(self, tracefunc):
        """Set a function to be called every time the display updates."""
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
    """Define shared methods for listbox-type classes.

    Public Methods: get_selected
    """

    def get_selected(self):
        """Return a list of currently selected items."""
        index = self.listbox.curselection()
        selected = []
        for i in index:
            selected.append(self.listbox.get(i))
        return selected


class VarWindow(Window):
    """Create window to select the items of a condition.

    Public Methods: build_box, filter

    Public Attributes:
    object -- the frame everything that attatched to
    listbox -- the Listbox object that displays the array
    """

    def build_box(self, condition):
        """Change the contents displayed.

        Arguments:
        condition -- the condition object you want to display
        """
        self.condition = condition
        varlist = self.condition.array
        self.listbox.delete(0, "end")
        for i in range(len(varlist)):
            self.listbox.insert(i, varlist[i])

    def filter(self, string):
        """Filter the contents by some string.

        Arguments:
        string -- the string to filter by
        """
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
    """Display and store selected items.

    Public Methods: add, remove

    Public Attributes:
    object -- the frame everything is attatched to
    listbox -- the Listbox object that displays the contents
    """

    def add(self, varlist):
        """Add items from a list that are not already displayed."""
        allvars = self.listbox.get(0, last="end")
        for var in varlist:
            if var not in allvars:
                self.listbox.insert(self.listbox.size(), var)

    def remove(self, *args):
        """Remove all currently selected items."""
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
    """Enter and trace filter strings.

    Public Methods: get_filter, add_trace

    Public Attributes:
    object -- the frame everything is attatched to
    """

    def get_filter(self):
        """Return the current filter."""
        return self._filter.get()

    def add_trace(self, tracefunc):
        """Set a function to execute every time the filter changes."""
        self._filter.trace_add("write", tracefunc)

    def __init__(self, frame):
        self.object = Frame(frame)
        self._label = Label(self.object, text="Filter: ").pack(side="left")
        self._filter = StringVar()
        self._entry = Entry(self.object,
            textvariable=self._filter).pack(side="right")


class VarSelector(TkWidget):
    """Insert a gui for selecting specific data filters for the case data.

    Public Methods: add

    Public Attributes:
    object -- the frame everything is attatched to

    *Notes: Enter and BackSpace are keyboard shortcuts for add and remove
    """

    def add(self, *args):
        """Add all selected items to the display window."""
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
