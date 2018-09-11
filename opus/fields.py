# -*- coding: utf-8 -*-
import re

from .data import DataDict

def splitKey(key):
    '''Split from first uppercase word (ie., `body`)'''
    body = re.findall('[^a-z]+', key)[0]
    field = key.split(body)[1]
    return body, field


class Field(object):
    def __init__(self, field, json):
        if len(json) == 0:
            raise KeyError('Unknown field `{}`'.format(field))

        self._json = json
        self.field = field
        self.label = json['label']
        self.category = json['category']
        self.slug = json['slug']
        self.old_slug = json['old_slug']

    def __repr__(self):
        return '{} ({}):\n => Category {} / Slug: {}'.format(self.label, self.field, self.category, self.slug)

    def __str__(self):
        return self.label

class Fields(DataDict):
    def __init__(self, json):
        DataDict.__init__(self)
        self._json = json
        for key, value in json.items():
            self.append(key.lower(), Field(key, value))

    def __repr__(self):
        return 'OPUS API list of all fields available ({}):\n'.format(len(self)) + \
               '\n'.join(' - {}'.format(key) for key in self)
