"""Description of the Ames Housing dataset.

This module uses the information available on the publication homepage and
defines a nested dictionary `ALL_COLUMNS` that can be used to decode the data
in the accompanying AmesHousing.xls file in the data folder. For convenience,
`ALL_VARIABLES` provides a list of only the column names.

Furthermore, six helper dictionaries `CONTINUOUS_COLUMNS`, `DISCRETE_COLUMNS`,
`NUMERIC_COLUMNS`, `NOMINAL_COLUMNS`, `ORDINAL_COLUMNS`, and `LABEL_COLUMNS`
are defined that provide just the subset of the columns with the corresponding
data types. Note that the numeric dictionary unifies the continuous and
discrete data columns while the label dictionary unifies the nominal and
ordinal columns. For each of the six dictionaries, a list of the actual column
names is created with the same name and the suffix "_VARIABLES" instead of
"_COLUMNS", e.g., "CONTINUOUS_VARIABLES" instead of "CONTINUOUS_COLUMNS".

Lastly, the LABEL_TYPES list can be used to quickly check types in a readable
way.

Source:
    https://www.amstat.org/publications/jse/v19n3/decock/DataDocumentation.txt

Implementation Note:
    This file defines the "constants" it exports dynamically. This is a bit
    advanced but intentional!
"""
# pragma pylint:disable=W0603

import re

import requests


LABEL_TYPES = ["nominal", "ordinal"]
# Note that these dictionaries and lists are not actually constants but
# filled in during import time which makes them "near"-constant.
ALL_COLUMNS = {}
ALL_VARIABLES = []
CONTINUOUS_COLUMNS = {}
CONTINUOUS_VARIABLES = []
DISCRETE_COLUMNS = {}
DISCRETE_VARIABLES = []
NUMERIC_COLUMNS = {}
NUMERIC_VARIABLES = []
NOMINAL_COLUMNS = {}
NOMINAL_VARIABLES = []
ORDINAL_COLUMNS = {}
ORDINAL_VARIABLES = []
LABEL_COLUMNS = {}
LABEL_VARIABLES = []


def _get_lines():
    """Obtain the non-empty lines of the data description file."""
    # Read cached data file.
    try:
        with open("data_documentation.txt", "r") as file:
            lines = file.readlines()
    # If there is no cached file, obtain in from the original source.
    except FileNotFoundError:
        response = requests.get(
            "https://www.amstat.org/publications"
            "/jse/v19n3/decock/DataDocumentation.txt"
        )
        # Cache the retrieved file.
        with open("data_documentation.txt", "w") as file:
            file.write(response.text)
        lines = response.text.split("\r\n")
    # Remove header, footer, and empty lines.
    lines = [x.replace("  ", " ").strip() for x in lines[13:545]]
    lines = [x for x in lines if x != ""]

    return lines


def _extract_meta_data(lines):
    """Extract variables and realizations for a line.

    This function parses the lines from the data documentation file and
    writes the results into the global dictionary ALL_COLUMNS that is exported
    by this module.

    A line can be a variable consisting of:
        - the name of the variable / column,
        - the variable's type (continuous, discrete, nominal, or ordinal), and
        - a text description of the variable.

    A line can also be a realization of a label column consisting of:
        - the encoding,
        - and the description.

    Implementation note:
        As the lines come in order, the "elif" condition below correctly refers
        to the last line representing a variable.
    """
    variable = re.compile(r"^(.*)(?:[\s]+)\(([\w]*)\)(?:\t)?: (.*)$")
    realization = re.compile(r"^(.*)\t(.*)$")
    # The two ID columns and the target variable "SalePrice"
    # are not put into the helper dicts / lists as they are
    # treated seperately in the modelling anyways.
    non_feature_columns = ["Order", "PID", "SalePrice"]

    for line in lines:
        # Process the next variable in the list.
        match = variable.match(line)
        if match:
            name, type_, description = match.groups()
            # Skip the non-feature columns (that are always non-label columns).
            if name in non_feature_columns:
                continue
            # name = name.strip()
            type_ = type_.lower()
            # description = description.strip()
            # Create an entry for the next variable in the list.
            ALL_COLUMNS[name] = {"type": type_, "description": description}
            # Only if the variable is a label type, a lookup table is needed.
            if type_ in LABEL_TYPES:
                ALL_COLUMNS[name].update({"lookups": {}})
            # Ordinal variables also store the order of their realizations
            # exactly as defined in the data description file.
            if type_ == 'ordinal':
                ALL_COLUMNS[name].update({"order": []})
        # Add label realizations to a previously found label variable.
        elif type_ in LABEL_TYPES:
            match = realization.match(line)
            code, description = match.groups()
            code = code.strip()
            ALL_COLUMNS[name]["lookups"][code] = description
            if type_ == 'ordinal':
                ALL_COLUMNS[name]["order"].append(code)


def _populate_dicts_and_lists():
    """Populate all "secondary" dictionaries and lists.

    The ALL_COLUMNS dictionary is the "main" dictionary and all other global
    dictionaries and lists are considered derived from it and thus considered
    "secondary".
    """
    global ALL_VARIABLES
    global CONTINUOUS_COLUMNS
    global CONTINUOUS_VARIABLES
    global DISCRETE_COLUMNS
    global DISCRETE_VARIABLES
    global NUMERIC_COLUMNS
    global NUMERIC_VARIABLES
    global NOMINAL_COLUMNS
    global NOMINAL_VARIABLES
    global ORDINAL_COLUMNS
    global ORDINAL_VARIABLES
    global LABEL_COLUMNS
    global LABEL_VARIABLES
    # The global data structures are not re-assigned to so as to keep all
    # references in the Jupyter notebooks alive. Instead, they are emptied
    # and re-filled.
    ALL_VARIABLES[:] = sorted(ALL_COLUMNS)
    CONTINUOUS_COLUMNS.clear()
    CONTINUOUS_COLUMNS.update(
        {
            key: value
            for (key, value) in ALL_COLUMNS.items()
            if value["type"] == "continuous"
        }
    )
    CONTINUOUS_VARIABLES[:] = sorted(CONTINUOUS_COLUMNS)
    DISCRETE_COLUMNS.clear()
    DISCRETE_COLUMNS.update(
        {
            key: value
            for (key, value) in ALL_COLUMNS.items()
            if value["type"] == "discrete"
        }
    )
    DISCRETE_VARIABLES[:] = sorted(DISCRETE_COLUMNS)
    NUMERIC_COLUMNS.clear()
    NUMERIC_COLUMNS.update({**CONTINUOUS_COLUMNS, **DISCRETE_COLUMNS})
    NUMERIC_VARIABLES[:] = sorted(NUMERIC_COLUMNS)
    NOMINAL_COLUMNS.clear()
    NOMINAL_COLUMNS.update(
        {
            key: value
            for (key, value) in ALL_COLUMNS.items()
            if value["type"] == "nominal"
        }
    )
    NOMINAL_VARIABLES[:] = sorted(NOMINAL_COLUMNS)
    ORDINAL_COLUMNS.clear()
    ORDINAL_COLUMNS.update(
        {
            key: value
            for (key, value) in ALL_COLUMNS.items()
            if value["type"] == "ordinal"
        }
    )
    ORDINAL_VARIABLES[:] = sorted(ORDINAL_COLUMNS)
    LABEL_COLUMNS.clear()
    LABEL_COLUMNS.update({**NOMINAL_COLUMNS, **ORDINAL_COLUMNS})
    LABEL_VARIABLES[:] = sorted(LABEL_COLUMNS)


def _rename_column(old_name, new_name):
    """Change the name of a column."""
    global ALL_COLUMNS
    ALL_COLUMNS[new_name] = ALL_COLUMNS[old_name]
    del ALL_COLUMNS[old_name]


def correct_column_names(data_columns):
    """Cross-check the column names between data and description file.

    In rare cases, the variable name in the data description file was slightly
    changed, i.e., a dash or a space needs to be removed.

    This function adjusts the keys in all the dictionaries and lists.
    """
    for desc_column in ALL_VARIABLES:
        if desc_column not in data_columns:
            for data_column in data_columns:
                # Column name was truncated in description file.
                if data_column.startswith(desc_column):
                    _rename_column(desc_column, data_column)
                    break
                # Spaces between words in Excel were removed.
                adj_data_column = data_column.replace(" ", "")
                if adj_data_column == desc_column:
                    _rename_column(desc_column, data_column)
                    break
                # Spaces between words in description file were removed.
                adj_desc_column = desc_column.replace(" ", "")
                if adj_data_column == adj_desc_column:
                    _rename_column(desc_column, data_column)
                    break
                # Dashes in description file were removed.
                adj_desc_column = desc_column.replace("-", "")
                if data_column == adj_desc_column:
                    _rename_column(desc_column, data_column)
                    break
    # Propagate the change to all "secondary" dictionaries and lists.
    _populate_dicts_and_lists()


# This code is executed once during import time and
# populates all the "constants" directly or indirectly.
_extract_meta_data(_get_lines())
_populate_dicts_and_lists()
