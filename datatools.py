"""A set of tools to contain and manipulate data.

Contains:
* cases -- dataframe containing all case data
* Condition -- data container class of a specific condition in cases
* condition_dict -- dictionary for retrieving condition class from name
* load_data -- function that attempts to load data at a specified path
* condition_list -- list of condition objects in use
* defaultCondition -- condition object to default to
* filter_cases -- filter case data with a set of filters
"""

import pandas as pd
import numpy as np

_condition_tup = (
"Species", "Admit. Life Stage", "Rescue Jurisdiction",
"Circumstances of Rescue", "Injury", "Disposition", "Disposition Addit.",
"Disposition Jurisdiction", "To Whom"
)
_toy_data = np.repeat("None", len(_condition_tup)).reshape(1, 9)
# Toy data to make the program run when real data is not loaded

def load_data(datapath):
    """Attept to load data at a specified path. Loads toy data if it fails

    Arguments:
    datapath -- the path of the file to load
    """
    global cases
    print("loading case data...")
    try:
        cases = pd.read_html(datapath)[0]
    except ValueError:
        print("data not found, loading toy data...")
        cases = pd.DataFrame(_toy_data, columns=_condition_tup)

_datapath = "C:/Users/buffs/Documents/cases.xls"
load_data(_datapath)

condition_dict = {}
# Retrieve a condition object from its string name

class Condition:
    """Store the case data of a specific data heading.

    name -- the string name of the data header.
    isgrouped -- whether each case entry has multiple values separated by " / ".
    series -- the corresponding series in cases with null values removed.
    array -- the series as an array-like object with duplicates removed.
    df -- (only for grouped data) a dataframe acting as a truth table
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

        condition_dict[self.name] = self

print("processing case data...")
condition_list = [
Condition("Species"), Condition("Admit. Life Stage"),
Condition("Rescue Jurisdiction"),
Condition("Circumstances of Rescue", isgrouped=True),
Condition("Injury", isgrouped=True), Condition("Disposition"),
Condition("Disposition Addit."), Condition("Disposition Jurisdiction"),
Condition("To Whom"),
]
# List of all condition objects in use
defaultCondition = condition_list[0]
# Condition object to default to
print("done\n")

def _single_filter_indicies(filter):
    condition_name, item = filter
    condition = condition_dict[condition_name]
    if condition.isgrouped:
        indicies = cases[condition.df[item]].index
    else:
        indicies = cases[lambda df: df[condition_name] == item].index
    return indicies


def filter_cases(filters):
    """Filter cases by list of selected filters.

    Arguments:
    filters -- list of selected filters
        - Should be of the form [(condition, item), (condition, item)]
    """
    index_dict = {}
    # Temporarily stores indicies

    for filter in filters:
        # Initializes a list in index_dict for each condition name in filters
        condition_name, item = filter
        index_dict[condition_name] = []

    for filter in filters:
        # Appends a list of indicies from filtering each individual item
        # into the list that corresponds to the condition name in index_dict
        indicies = _single_filter_indicies(filter)
        condition_name, _ = filter
        index_dict[condition_name].append(indicies)

    print(index_dict)

    for condition_name, indicies in index_dict.items():
        # Consolodates each list of lists in index_dict into one list
        if len(indicies) == 0:
            index_dict[condition_name] = []
        else:
            index_dict[condition_name] = set(indicies[0]).union(*indicies)

    condition_indicies = list(index_dict.values())
    if len(condition_indicies) == 0:
        filtered_indicies = []
    else:
        filtered_indicies = set(condition_indicies[0]).intersection(*condition_indicies)
    filtered_indicies = list(filtered_indicies)
    return cases.iloc[filtered_indicies]
    # Intersects all lists in index_dict and returns the case data
    # at those indicies

filters = [
("Species", "Great Horned Owl"),
("Injury", "Skeleton"),
]
