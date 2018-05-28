# -*- coding: utf-8 -*-

class Range(object):
    def __init__(self, field, json):
        self.max = float(json['max'])
        self.min = float(json['min'])
        self.nulls = int(json['nulls'])
        self._field = field

    def __repr__(self):
        return 'OPUS API Range endpoints for field: {}'.format(self._field)
