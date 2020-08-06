import pandas as pd

from field import Field, MetaField

class Product:
    def __init__(self):
        self.fields = []

    @property
    def fields(self):
        return self.__fields

    @fields.setter
    def fields(self, fields):
        for field in fields:
            if not isinstance(field, (Field, MetaField)):
                raise TypeError(f"field is '{type(field)}' object. Should be one of these types: Field, MetaField")

            self.fields.append(field)

    def add_field(self, field):
        if not isinstance(field, (Field, MetaField)):
            raise TypeError(f"field is '{type(field)}' object. Should be one of these types: Field, MetaField")

        self.fields.append(field)

    def to_serie(self):
        pass

