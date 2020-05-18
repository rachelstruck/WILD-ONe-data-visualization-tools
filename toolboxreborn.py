from tkinter import *
from datatools import *


class ConditionSelect(Menubutton):
    """Create a menu button to select a particular condition.

    Arguments:
    frame -- the tkinter parent window

    Public Methods: get, set, update_display, get_condition, set_tracefunc.
    get and set extend the get and set methods on the displayed string
    variable.
    """

    def update_display(self, name):
        """Set the name that the button displays and call the trace function.

        Arguments:
        name -- the string to be displayed by the button
        """
        self.set(name)
        if self.tracefunc is not None:
            self.tracefunc()
    def _update_display_command(self, name):
        return lambda: self.update_display(name)

    def get_condition(self):
        """Return the condition object currently displayed."""
        name = self.get()
        return condition_dict[name]

    def set_tracefunc(self, tracefunc):
        """Set a function to be called every time the display updates."""
        self.tracefunc = tracefunc

    def __init__(self, parent):
        self._stringvar = StringVar()
        self.get = self._stringvar.get
        self.set = self._stringvar.set
        self.set(defaultCondition.name)

        self.tracefunc = None

        Menubutton.__init__(
            self, parent, textvariable=self._stringvar, relief="raised")
        self._menu = Menu(self, tearoff=0)
        self["menu"] = self._menu

        for condition in condition_list:
            self._menu.add_command(
                label=condition.name,
                command=self._update_display_command(condition.name))


class VarWindow(Frame):
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

    def get_selected(self):
        """Return a list of currently selected items."""
        index = self.listbox.curselection()
        selected = []
        for i in index:
            selected.append(self.listbox.get(i))
        return selected

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self._sbar = Scrollbar(self)
        self.listbox = Listbox(
            self, yscrollcommand=self._sbar.set,
            width=50, height=19, selectmode="extended")
        self.listbox.pack(side="left")
        self._sbar.pack(side="right", fill="y")
        self._sbar.config(command=self.listbox.yview)

        self.build_box(defaultCondition)


class SelectedWindow(Frame):
    """Display and store selected items.

    Public Methods: add, remove

    Public Attributes:
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

    def get_displayed(self):
        """Return the contents of the listbox."""
        return self.listbox.get(0, last="end")

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.listbox = Listbox(self, width=50, height=19,
                               selectmode="extended")
        self.listbox.pack()


class Filter(Frame):
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

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self._label = Label(self, text="Filter: ").pack(side="left")
        self._filter = StringVar()
        self._entry = Entry(self,
            textvariable=self._filter).pack(side="right")


class VarSelector(Frame):
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

    def get_selected(self):
        return self._selected_window.get_displayed()

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self._condition_selector = ConditionSelect(self)
        self._condition_selector.grid(row=0, column=0)
        self._condition_selector.set_tracefunc(self._condition_trace)
        self._var_window = VarWindow(self)
        self._var_window.grid(row=1, column=0)
        self._selected_window = SelectedWindow(self)
        self._selected_window.grid(row=1, column=1)
        print(type(self._selected_window))
        self._add_button = Button(
            self, text="Add Variable",
            command=self.add).grid(row=2, column=0)
        self._remove_button = Button(
            self, text="Remove Variable",
            command=self._selected_window.remove).grid(row=2, column=1)
        self._filter = Filter(self)
        self._filter.grid(row=3, column=0)
        self._filter.add_trace(self._filter_trace)

        self._var_window.listbox.bind("<Return>", self.add)
        self._selected_window.listbox.bind("<BackSpace>",
                                           self._selected_window.remove)


if __name__ == "__main__":

    root = Tk()
    VarSelector(root).pack()
    root.mainloop()
