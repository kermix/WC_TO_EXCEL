import pandas as pd

from field import Field, MetaField, VariantAttributeField

from field_filters import *


# Project is optimised for BioCompare DB format

def get_header_from_field_set(fields):
    importance_levels = []
    field_header = []
    for field in fields:
        importance_levels.append(field.importance_level)
        field_header.append(field.field_name)
    return pd.MultiIndex.from_arrays((importance_levels, field_header))


def get_required_field_set():
    return [Field(key_name='name', importance_level="Required", field_name='Name'),
    VariantAttributeField(variant_names=('sku',), optional_meta_name='sku', importance_level="Required", field_name='Catalog Number'),
    Field(key_name='permalink', importance_level="Required", field_name='URL'),
    VariantAttributeField(variant_names=('Classes', 'Quantity', 'Exctractions', 'Unit', 'Reactions',
                                         'Weight', 'Volume', 'Size'),
                          optional_meta_name='quantity', importance_level="Required", field_name='Quantity')]


def get_enzymes_field_set():
    return get_required_field_set() + [
        Field(key_name='price', importance_level='Recommended', field_name='Euro price', variant_field=True),
        MetaField(key_name="enzyme_family", importance_level="Recommended", field_name="Enzyme Family (Enzymes only)"),
        MetaField(key_name="enzyme_name", importance_level="Recommended", field_name="Enzyme Subfamily (Enzymes only)"),
        MetaField(key_name="enzyme_features", importance_level="Recommended",
                  field_name="Enzyme Features (Enzymes only)"),
        MetaField(key_name="restriction_enzyme", importance_level="Recommended",
                  field_name="Restriction Enzyme (Enzymes only)"),
    ]


def get_extraction_kits_field_set():
    return get_required_field_set() + [
        Field(key_name='price', importance_level='Recommended', field_name='Euro price', variant_field=True),
        Field(key_name='description', importance_level='Optional', field_name='Description'),
        Field(key_name='category', importance_level='Optional', field_name='category'),
        Field(key_name='references', importance_level='Optional', field_name='Product-specific References'),
        MetaField(key_name='isolated_material', importance_level='Custom', field_name='Isolated Material'),
        MetaField(key_name='kit_components', importance_level='Custom', field_name='Extraction kits'),
        MetaField(key_name='purification_step', importance_level='Custom', field_name='Sample Material'),
        MetaField(key_name='efficiency', importance_level='Custom', field_name='Efficiency'),
        MetaField(key_name='binding_capacity', importance_level='Custom', field_name='Binding Capacity'),
        MetaField(key_name='time_required', importance_level='Custom', field_name='Time Required'),
        MetaField(key_name='yield_purity', importance_level='Custom', field_name='Yield Purity')
    ]

def get_extraction_columns_field_set():
    return get_required_field_set() + [
        Field(key_name='price', importance_level='Recommended', field_name='Euro price', variant_field=True),
        Field(key_name='description', importance_level='Optional', field_name='Description'),
        Field(key_name='category', importance_level='Optional', field_name='category'),
        Field(key_name='references', importance_level='Optional', field_name='Product-specific References'),
        MetaField(key_name='type', importance_level='Custom', field_name='Type ')
    ]