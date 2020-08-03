from settings import DEFAULT_FIELD_VALUE


class Field:
    def __init__(self, key_name="", importance_level="", field_name=""):
        if not isinstance(key_name, str) or not isinstance(importance_level, str) or not isinstance(field_name, str):
            raise TypeError("All parameters should be string")

        if not key_name or not importance_level or not field_name:
            raise ValueError("All parameters should be set")

        self.key_name = key_name
        self.importance_level = importance_level
        self.field_name = field_name
        self.value = DEFAULT_FIELD_VALUE

    def value_from_dict(self, dictionary, filter_func=None):
        if filter_func is not None and not callable(filter_func):
            raise TypeError(f'filter_func is {type(filter_func)} object and is not callable')

        try:
            self.value = dictionary[self.key_name]
            if filter_func is not None:
                self.value = filter_func(self.value)
        except KeyError:
            self.value = DEFAULT_FIELD_VALUE


class MetaField(Field):
    def value_from_dict(self, dictionary, filter_func=None):
        if filter_func is not None and not callable(filter_func):
            raise TypeError(f'filter_func is {type(filter_func)} object and is not callable')

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
