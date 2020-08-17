import pandas as pd

from field_sets import get_enzymes_field_set

from category_sets import CategorySet

# Project is optimised for BioCompare DB format

cs = CategorySet(categories=48, exclude=[1004, 991], fieldset=get_enzymes_field_set())
cs.populate_data()

df = cs.to_dataframe()