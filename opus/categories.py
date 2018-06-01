# -*- coding: utf-8 -*-

from .data import DataDict

class Category(object):
    def __init__(self, json):
        self.name = json['table_name']
        self.label = json['label']
                
    def __repr__(self):
        return '{} ({})'.format(self.label, self.name)


class Categories(DataDict):
    def __init__(self, json):
        DataDict.__init__(self)
        self._json = json
        for category in json:
            self.append(category['table_name'],  Category(category))

    def __repr__(self):
        return 'OPUS API list of all categories ({}):\n'.format(len(self)) + \
            '\n'.join(' - {}'.format(value) for value in self.values())