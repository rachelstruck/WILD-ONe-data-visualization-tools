"""Number of Cases Applet"""

from toolbox import *
from os import startfile


class NumOfCases(TkWidget):

    def _compile(self):
        filters = self._var_selector.get_selected()
        self._compiled_cases = filter_cases(filters)
        count = self._compiled_cases.shape[0]
        self._num_variable.set(count)

    def _open(self):
        if self._compiled_cases is not None:
            self._compiled_cases.to_csv("compiled cases.csv")
            startfile("compiled cases.csv")

    def __init__(self, frame):
        self.object = Frame(frame)
        self._var_selector = VarSelector(self.object)
        self._var_selector.grid(row=0, column=0)
        self._right_frame = Frame(self.object).grid(row=0, column=1)
        self._num_variable = IntVar()
        self._num_variable.set(np.nan)
        self._num_label = Label(self._right_frame,
                                textvariable=self._num_variable)
        self._num_label.grid(row=0, column=0)
        self._open_button = Button(
            self._right_frame, text="Open Compiled Data",
            command=self._open).grid(row=1, column=0)
        self._compile_button = Button(self._right_frame, text="Compile Data",
                                      command=self._compile)
        self._compile_button.grid(row=2, column=0)
        self._compiled_cases = None


if __name__ == "__main__":

    root = Tk()
    num_of_cases = NumOfCases(root).pack()
    root.mainloop()
