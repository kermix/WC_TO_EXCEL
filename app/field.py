from settings import DEFAULT_FIELD_VALUE

from copy import copy, deepcopy


class Field(object):
    def __init__(self, key_name="", importance_level="", field_name="", filter_func=None, variant_field=False):
        if not isinstance(key_name, str) or not isinstance(importance_level, str) or not isinstance(field_name, str):
            raise TypeError("All parameters should be string")

        if not key_name or not importance_level or not field_name:
            raise ValueError("All parameters should be set")

        self.key_name = key_name
        self.importance_level = importance_level
        self.field_name = field_name
        self.filter_func = filter_func
        self.value = DEFAULT_FIELD_VALUE
        self.__variant_field = variant_field

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def value_from_dict(self, dictionary):
        if self.filter_func is not None and not callable(self.filter_func):
            raise TypeError(f"self.filter_func is '{type(self.filter_func)}' object and is not callable")

        try:
            self.value = dictionary[self.key_name]
            if self.filter_func is not None:
                self.value = self.filter_func(self.value)
        except KeyError:
            self.value = DEFAULT_FIELD_VALUE

    def is_variant_field(self):
        return self.__variant_field


class MetaField(Field):
    def __init__(self, key_name="", importance_level="", field_name="", filter_func=None):
        super(MetaField, self).__init__(key_name, importance_level, field_name, filter_func)

    def value_from_dict(self, dictionary):
        if self.filter_func is not None and not callable(self.filter_func):
            raise TypeError(f"self.filter_func is '{type(self.filter_func)}' object and is not callable")

        if "meta_data" not in dictionary:
            raise KeyError("Key meta_data is not present in supplied dictionary.\n"
                           "Ensure this is product, not variant dictionary.")

        try:
            self.value = next((
                meta['value'] for meta in dictionary['meta_data']
                if 'key' in meta and meta['key'] == self.key_name and 'value' in meta
            ))
            if self.filter_func is not None:
                self.value = self.filter_func(self.value)
        except (KeyError, StopIteration):
            super(MetaField, self).value_from_dict(dictionary, self.filter_func)


class VariantAttributeField(MetaField):
    def __init__(self, variant_names="", optional_meta_name="", importance_level="", field_name="", filter_func=None,
                 all_attributes=False):
        if not isinstance(variant_names, (str, list, tuple)):
            raise TypeError(f"variant_names is '{type(variant_names)} object. It should be string or list.")

        if not variant_names:
            raise AttributeError("variant names should be set.")

        self.variant_names = variant_names
        self.has_fallback = False if not optional_meta_name else True
        self.all_attributes = all_attributes

        super(VariantAttributeField, self).__init__(
            key_name=" " if not self.has_fallback else optional_meta_name,
            importance_level=importance_level,
            field_name=field_name,
            filter_func=filter_func)

    def value_from_dict(self, variant_dictionary={}, field_dictionary={}):
        attributes = (
            attrib['option'] for attrib in variant_dictionary['attributes']
            if (
                       isinstance(self.variant_names, str) and
                       'name' in attrib and
                       attrib['name'] == self.variant_names and
                       'option' in attrib
               ) or (
                       isinstance(self.variant_names, (list, tuple)) and
                       'name' in attrib and
                       attrib['name'] in self.variant_names and
                       'option' in attrib
               )
        )
        if not self.all_attributes:
            try:
                self.value = next(attributes)

            except StopIteration:
                if self.has_fallback:
                    try:
                        super(VariantAttributeField, self).value_from_dict(variant_dictionary, self.filter_func)
                    except KeyError:
                        super(VariantAttributeField, self).value_from_dict(field_dictionary, self.filter_func)
        else:
            self.value = " ".join(attributes)

        if self.filter_func is not None:
            self.value = self.filter_func(self.value)
