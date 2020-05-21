"""Pie Chart Applet"""

from toolbox import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class PieChart(Frame):

    def _compile(self):
        self._ax.clear()
        filters = self._var_selector.get_selected()
        compiled_cases = filter_cases(filters)
        condition = self._condition_select.get_condition()
        series = compiled_cases[condition.name].dropna()

        count_list = [series[lambda x: x == i].count()
                      for i in condition.array]
        count_series = pd.Series(count_list, index=condition.array)
        count_series_sorted = count_series.sort_values(ascending=False)
        sum = count_series.sum()
        count_series_percent = count_series_sorted/sum * 100
        count_series_percent = round(count_series_percent, 1)

        labels = []
        for num, label in zip(
                count_series_sorted.array, count_series_sorted.index):
            if num / sum >= 0.02:
                labels.append(label)
            else:
                labels.append("")

        self._ax.pie(count_series_sorted.array, labels=labels)
        self._canvas.draw()

        self._listbox.delete(0, last="end")
        for name, number, percent in zip(
                count_series_sorted.index, count_series_sorted.array,
                count_series_percent.array):
            self._listbox.insert(
                self._listbox.size(), f"{percent}%    {number}    {name}")

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self._var_selector = VarSelector(self)
        self._var_selector.grid(row=0, column=0)
        self._right_frame = Frame(self)
        self._right_frame.grid(row=0, column=1)
        self._figure = Figure(figsize=(4, 3), dpi=100)
        self._ax = self._figure.add_subplot(111)
        self._canvas = FigureCanvasTkAgg(
            self._figure, master=self._right_frame)
        self._canvas.get_tk_widget().pack()
        self._condition_select = ConditionSelect(self._right_frame)
        self._condition_select.pack()
        self._compile_button = Button(
            self._right_frame, text="Compile Data", command=self._compile)
        self._compile_button.pack()
        self._listbox = Listbox(self, width=50, height=19)
        self._listbox.grid(row=0, column=2)


if __name__ == "__main__":

    root = Tk()
    PieChart(root).pack()
    root.mainloop()
