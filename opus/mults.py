# -*- coding: utf-8 -*-

class Mults(object):
    def __init__(self, json):
        self._field = json['field']
        self._data = json['mults']

    def __repr__(self):
        return 'OPUS API Mults for field: {}'.format(self._field)

    def __getitem__(self, attr):
        return self._data[attr]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def keys(self):
        return self._data.keys()

    def items(self):
        return self._data.items()

    def values(self):
        return self._data.values()
