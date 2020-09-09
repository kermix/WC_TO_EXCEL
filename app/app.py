import pandas as pd

from field_sets import get_enzymes_field_set, \
    get_extraction_kits_field_set, \
    get_extraction_columns_field_set, \
    get_amplification_kits_field_set, \
    get_reverse_transcription_kits_field_set, \
    get_chemicals_and_reagents_field_set, \
    get_electrophoresis_ladders_field_set, \
    get_agaroses_field_set

from category_sets import CategorySet

from misc import merge_db

# Project is optimised for BioCompare DB format

sets = [
    (CategorySet(categories=48, exclude=[1004, 991, 4961], fieldset=get_enzymes_field_set()),
     "Enzymes",
     "enzymes.xlsx"),
    ]


for cs, sheet_name, file_name in sets:
    cs.populate_data()
    df = cs.to_dataframe()
    df["Required", "Item Name"] = df.loc[:, ("Required", ("Item Name", "Variant Name"))].apply(lambda x: ' - '.join(x) if x[1] else x[0], axis=1)
    df = df.drop('Variant Name', axis=1, level=1)
    cs.save(df=df, filename=file_name, sheet_name=sheet_name)

merge_db("database")
