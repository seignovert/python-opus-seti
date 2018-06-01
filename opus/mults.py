# -*- coding: utf-8 -*-

from .data import DataDict

class Mults(DataDict):
    def __init__(self, json):
        DataDict.__init__(self)
        self._field = json['field']
        self.load(json['mults'])

    def __repr__(self):
        return 'OPUS API Multiple choice for field: `{}`\n'.format(self._field) + \
               '\n'.join(' - {} : {}'.format(key, value) for key, value in self.items())
