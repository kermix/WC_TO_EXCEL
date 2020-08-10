from settings import DEFAULT_FIELD_VALUE

from copy import copy, deepcopy

class Field(object):
    def __init__(self, key_name="", importance_level="", field_name=""):
        if not isinstance(key_name, str) or not isinstance(importance_level, str) or not isinstance(field_name, str):
            raise TypeError("All parameters should be string")

        if not key_name or not importance_level or not field_name:
            raise ValueError("All parameters should be set")

        self.key_name = key_name
        self.importance_level = importance_level
        self.field_name = field_name
        self.value = DEFAULT_FIELD_VALUE

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

    def value_from_dict(self, dictionary, filter_func=None):
        if filter_func is not None and not callable(filter_func):
            raise TypeError(f"filter_func is '{type(filter_func)}' object and is not callable")

        try:
            self.value = dictionary[self.key_name]
            if filter_func is not None:
                self.value = filter_func(self.value)
        except KeyError:
            self.value = DEFAULT_FIELD_VALUE


class MetaField(Field):
    def value_from_dict(self, dictionary, filter_func=None):
        if filter_func is not None and not callable(filter_func):
            raise TypeError(f"filter_func is '{type(filter_func)}' object and is not callable")

        if "meta_data" not in dictionary:
            raise KeyError("Key meta_data is not present in supplied dictionary.\n"
                           "Ensure this is product, not variant dictionary.")

        try:
            self.value = next((
                meta['value'] for meta in dictionary['meta_data']
                if 'key' in meta and meta['key'] == self.key_name and 'value' in meta
            ), DEFAULT_FIELD_VALUE)
            if filter_func is not None:
                self.value = filter_func(self.value)
        except KeyError:
            self.value = DEFAULT_FIELD_VALUE

class VariantAttributeField(MetaField):
    def __init__(self, variant_names="", optional_meta_name="", importance_level="", field_name=""):
        if not isinstance(variant_names, (str, list, tuple)):
            raise TypeError(f"variant_names is '{type(variant_names)} object. It should be string or list.")

        if not variant_names:
            raise AttributeError("variant names should be set.")

        self.variant_names = variant_names
        self.has_meta_fallback = False if not optional_meta_name else True


        super(VariantAttributeField, self).__init__(
            key_name=" " if not self.has_meta_fallback else optional_meta_name,
            importance_level=importance_level,
            field_name=field_name)

    def value_from_dict(self, variant_dictionary, field_dictionary, filter_func=None):
        try:
            self.value = next((
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
            ))
        except StopIteration:
            if self.has_meta_fallback:
                super(VariantAttributeField, self).value_from_dict(field_dictionary, filter_func)
            self.value = DEFAULT_FIELD_VALUE
