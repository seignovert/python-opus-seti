# -*- coding: utf-8 -*-

class Category(object):
    def __init__(self, json):
        self.name = json['table_name']
        self.label = json['label']
                
    def __repr__(self):
        return '`{}` -> {}'.format(self.name, self.label)


class Categories(object):
    def __init__(self, json):
        self._json = json
        self._data = {}
        for category in json:
            self._data[category['table_name']] = Category(category)

    def __repr__(self):
        return 'OPUS API list of all categories ({}):\n'.format(len(self)) + \
            '\n'.join(
               ' - {} ({})'.format(value.label, key) for key, value in self.items()
            )

    def __len__(self):
        return len(self._json)

    def __getitem__(self, attr):
        return self._data[attr.lower()]

    def __iter__(self):
        return iter(self._data)

    def keys(self):
        return self._data.keys()

    def items(self):
        return self._data.items()

    def values(self):
        return self._data.values()

