import pandas as pd

from field import Field, MetaField, VariantAttributeField

from copy import copy, deepcopy

class Product:
    def __init__(self):
        self.__fields = []

    @property
    def fields(self):
        return self.__fields

    @fields.setter
    def fields(self, fields):
        for field in fields:
            if not isinstance(field, (Field, MetaField, VariantAttributeField)):
                raise TypeError(f"field is '{type(field)}' object. Should be one of these types: "
                                f"Field, MetaField, VariantAttributeField")

            self.__fields.append(copy(field))

    def add_field(self, field):
        if not isinstance(field, (Field, MetaField, VariantAttributeField)):
            raise TypeError(f"field is '{type(field)}' object. Should be one of these types: "
                            f"Field, MetaField, VariantAttributeField")

        self.__fields.append(copy(field))

    def to_serie(self):
        importance_levels = [field.importance_level for field in self.fields]
        headers = [field.field_name for field in self.fields]

        serie = pd.Series(index=pd.MultiIndex.from_arrays((importance_levels, headers)))

        for field in self.fields:
            serie[field.importance_level, field.field_name] = field.value

        return serie

