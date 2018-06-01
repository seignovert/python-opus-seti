# -*- coding: utf-8 -*-

from .data import DataDict

class Range(DataDict):
    def __init__(self, field, json):
        DataDict.__init__(self)
        self._field = field
        self.append('min', float(json['min']))
        self.append('max', float(json['max']))
        self.append('null', int(json['nulls']))

    def __repr__(self):
        return 'OPUS API Range endpoints for field: `{}`\n'.format(self._field) + \
               '\n'.join(' - {} : {}'.format(key, value) for key, value in self.items())
