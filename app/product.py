import pandas as pd

from field import Field, MetaField

class Product:
    def __init__(self):
        self.fields = []

    def add_field(self, field):
        if not isinstance(field, (Field, MetaField)):
            raise TypeError(f"field is '{type(field)}'should be one of these types: Field, MetaField")

        self.fields.append(field)

    def to_serie(self):
        pass