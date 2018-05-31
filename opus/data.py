# -*- coding: utf-8 -*-

class DataDict(object):
    def __init__(self):
        self._data = {}

    def __repr__(self):
        return '<OPUS API generic class for data objects>'

    def __len__(self):
        return len(self._data)

    def __getitem__(self, attr):
        return self._data[attr]

    def __iter__(self):
        return iter(self._data)

    def keys(self):
        return self._data.keys()

    def items(self):
        return self._data.items()

    def values(self):
        return self._data.values()

    def append(self, key, value):
        self._data[key] = value

    def load(self, dict):
        self._data = dict

class Data(DataDict):
    def __init__(self, json):
        DataDict.__init__(self)
        self._json = json
        for row in json['page']:
            el = DataElement(self.columns, row)
            self._data[str(el)] = el

    def __repr__(self):
        return 'OPUS API Data objects (with {} elements):\n'.format(len(self)) + \
               '\n'.join(' - {}'.format(key) for key, _ in self.items())

    @property
    def count(self):
        return int(self._json['count'])

    @property
    def limit(self):
        return int(self._json['limit'])

    @property
    def order(self):
        return self._json['order']

    @property
    def page_no(self):
        return int(self._json['page_no'])

    @property
    def labels(self):
        return self._json['labels']

    @property
    def columns(self):
        return self._json['columns']


class DataElement(DataDict):
    def __init__(self, columns, row):
        DataDict.__init__(self)
        self._columns = columns
        self._row = row
        self._id = None
        for column, value in zip(columns, row):
            if 'Ring Observation ID' in column:
                self._id = value
            else:
                self.append(column, value)

        if self._id is None:
            raise KeyError('`Ring Observation ID` key is missing in `cols` query')

    def __repr__(self):
        return 'Ring Observation ID: {}\n'.format(str(self)) + \
               '\n'.join(' - {}: {}'.format(key, value) for key, value in self.items())

    def __str__(self):
        return self._id
