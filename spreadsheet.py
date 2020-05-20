"""Spreadsheet Applet"""

from toolbox import *
import webbrowser as wb
import threading
import time

class Spreadsheet(Frame):

    def _compile_thread(self, index_matrix, index, column_matrix, columns):
        intersect_matrix = index_matrix.T @ column_matrix
        intersect_frame = pd.DataFrame(intersect_matrix, index=index,
                                       columns=columns)
        self._intersect_frame = intersect_frame

        self._stop_processing()
        print("done\n")
        self._open()

    def _start_processing_anim(self):
        self._is_processing = True
        num_dots = 0
        while self._is_processing:
            self._processing_var.set("processing" + "."*num_dots)
            num_dots += 1
            num_dots %= 4
            time.sleep(0.5)

    def _stop_processing(self):
        self._is_processing = False
        self._allow_compile = True
        self._processing_var.set("done")

    def _compile(self):
        if not self._allow_compile:
            print("NO")
            return
        self._allow_compile = False
        print("processing...")
        filters = self._var_selector.get_selected()
        daterange = self._var_selector.get_daterange()
        compiled_cases = filter_cases(filters, daterange=daterange)

        index_condition = self._condition_select_1.get_condition()
        index = index_condition.array
        index_matrix = index_condition.df.values.astype(int)
        column_condition = self._condition_select_2.get_condition()
        columns = column_condition.array
        column_matrix = column_condition.df.values.astype(int)

        t_compile = threading.Thread(
            target=self._compile_thread,
            args=(index_matrix, index, column_matrix, columns)
            )
        t_anim = threading.Thread(target=self._start_processing_anim)

        t_compile.start()
        t_anim.start()

    def _open(self):
        if self._intersect_frame is not None:
            self._intersect_frame.to_csv("spreadsheet_output.csv")
            wb.open("spreadsheet_output.csv")

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self._intersect_frame = None
        self._var_selector = VarSelector(self)
        self._var_selector.grid(row=0, column=0)
        self._right_frame = Frame(self)
        self._right_frame.grid(row=0, column=1)
        self._condition_select_1 = ConditionSelect(self._right_frame)
        self._condition_select_1.pack()
        self._condition_select_2 = ConditionSelect(self._right_frame)
        self._condition_select_2.pack()
        self._open_button = Button(
            self._right_frame, text="Open Compiled Data",
            command=self._open)
        self._open_button.pack()
        self._compile_button = Button(
            self._right_frame, text="Compile Data", command=self._compile)
        self._compile_button.pack()
        self._processing_var = StringVar()
        self._processing_var.set("")
        self._processing_label = Label(
            self._right_frame, textvariable=self._processing_var)
        self._processing_label.pack()
        self._is_processing = False
        self._allow_compile = True


if __name__ == "__main__":

    root = Tk()
    Spreadsheet(root).pack()
    root.mainloop()
