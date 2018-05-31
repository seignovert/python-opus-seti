# -*- coding: utf-8 -*-

import six
from datetime import datetime as dt

from .data import DataDict

def read_time(time):
    '''Read date time'''
    try:
        return dt.strptime(time, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        try:
            return dt.strptime(time, '%Y-%jT%H:%M:%S.%f')
        except ValueError:
            raise ValueError('Time `{}` does not match either `%Y-%m-%dT%H:%M:%S.%f` nor `%Y-%jT%H:%M:%S.%f`'.format(time))


class Metadata(DataDict):
    def __init__(self, json):
        DataDict.__init__(self)
        self._json = json
        for label, constraints in self._json.items():
            key = label.upper().replace(' ', '_').replace('_CONSTRAINTS', '')
            value = Constraints(key, constraints)
            self.append(key, value)

        self.ring_obs_id = self['GENERAL']['ring_obs_id']

    def __repr__(self):
        return 'OPUS API Metadata Ring observation: {}\n'.format(self.ring_obs_id) + \
               '\n'.join('\n{}'.format(values) for values in self.values())


class Constraints(DataDict):
    def __init__(self, name, constraints={}):
        DataDict.__init__(self)
        self.name = name
        for key, value in constraints.items():
            if key == 'is_image':
                value = (value == 1)
            
            if 'time' in key and isinstance(value, six.text_type):
                value = read_time(value)

            if value is not None and value != 'N/A' and value != -999:
                self.append(key, value)

    def __repr__(self):
        return '=> {} constraints\n' .format(self.name) + \
               '\n'.join(' - {}: {}'.format(key, value)
                         for key, value in self.items())
