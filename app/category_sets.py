import pandas as pd

from api import get_variants_as_products

from misc import to_comma_separated_string

class CategorySet:
    def __init__(self, categories, exclude, fieldset):
        self.categories = categories
        self.exclude = exclude
        self.fieldset = fieldset
        self.dataset = None

    def populate_data(self):
        categories = to_comma_separated_string(self.categories)
        exclude = to_comma_separated_string(self.exclude)
        self.dataset = get_variants_as_products(
                            fieldset=self.fieldset,
                            product_get_params={
                                "category": categories,
                                "exclude": exclude,
                            })

    def to_dataframe(self):
        df = pd.DataFrame()

        for product in self.dataset:
            series = product.to_series()
            df = df.append(series, ignore_index=True)
        return df

    def save(self, df=None, sheet_name="Sheet1", filename="dataset.xlsx"):
        if df is None:
            df = self.to_dataframe()

        df.to_excel(filename, sheet_name=sheet_name)


