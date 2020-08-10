from field import Field, MetaField, VariantAttributeField

from field_filters import *


# Project is optimised for BioCompare DB format

def get_header_from_field_set(self):
    importance_levels = []
    field_header = []
    for field in self.fields:
        importance_levels.append(field.importance_level)
        field_header.append(field.field_name)
    return importance_levels, field_header


def get_required_field_set():
    return [Field(key_name='name', importance_level="Required", field_name='Name'),
    VariantAttributeField(variant_names=('sku',), optional_meta_name='sku', importance_level="Required", field_name='Catalog Number'),
    Field(key_name='permalink', importance_level="Required", field_name='URL'),
    VariantAttributeField(variant_names=('Classes', 'Quantity', 'Exctractions', 'Unit', 'Reactions',
                                         'Weight', 'Volume'),
                          optional_meta_name='quantity', importance_level="Required", field_name='Quantity')]
