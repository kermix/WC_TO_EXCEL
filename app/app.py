import pandas as pd

from field_sets import get_enzymes_field_set

from category_sets import CategorySet

# Project is optimised for BioCompare DB format

sets = [
    (CategorySet(categories=48, exclude=[1004, 991, 4961], fieldset=get_enzymes_field_set()),
     "Enzymes",
     "enzymes.xlsx"),

    ]


for cs, sheet_name, file_name in sets:
    cs.populate_data()
    cs.save(filename=file_name, sheet_name=sheet_name)