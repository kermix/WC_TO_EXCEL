from field import Field, MetaField, VariantAttributeField

from field_filters import *


# Project is optimised for BioCompare DB format

def get_header_from_field_set(fields):
    importance_levels = []
    field_header = []
    for field in fields:
        importance_levels.append(field.importance_level)
        field_header.append(field.field_name)
    return importance_levels, field_header


def get_required_field_set():
    return [Field(key_name='name', importance_level="Required", field_name='Name'),
    VariantAttributeField(variant_names=('sku',), optional_meta_name='sku', importance_level="Required", field_name='Catalog Number'),
    Field(key_name='permalink', importance_level="Required", field_name='URL'),
    VariantAttributeField(variant_names=('Classes', 'Quantity', 'Exctractions', 'Unit', 'Reactions',
                                         'Weight', 'Volume', 'Size'),
                          optional_meta_name='quantity', importance_level="Required", field_name='Quantity')]

def get_enzymes_field_set():
    return get_required_field_set() + [
        MetaField(key_name="enzyme_family", importance_level="Recommended", field_name="Enzyme Family (Enzymes only)"),
        MetaField(key_name="enzyme_name", importance_level="Recommended", field_name="Enzyme Subfamily (Enzymes only)"),
        MetaField(key_name="enzyme_features", importance_level="Recommended",
                  field_name="Enzyme Features (Enzymes only)"),
        MetaField(key_name="restriction_enzyme", importance_level="Recommended",
                  field_name="Restriction Enzyme (Enzymes only)"),
    ]

