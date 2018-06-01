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

    def __repr__(self):
        if self.desc is not None:
            return '{} ({}):\n => {}\n {}'.format(self.label, self.field, self.desc, self.url)
        else:
            return '{}: ({})'.format(self.label, self.field)

    def __str__(self):
        return self.label

    @property
    def desc(self):
        desc = self._json['more_info']['def']
        if desc is False:
            return None
        else:
            return desc.replace('<br />', '')\
                       .replace('<br>', '')\
                       .replace('<Br>', '')\
                       .replace('\n', '')\
                       .replace('    ', ' ')\
                       .replace('  ', ' ')

    @property
    def url(self):
        url = self._json['more_info']['more_info']
        if url is False:
            return None
        else:
            return url


class Fields(DataDict):
    def __init__(self, json):
        DataDict.__init__(self)
        self._json = json
        self.append('GLOBAL', GlobalField())
        for key, value in json.items():
            if 'surfacegeometry' in key:
                try:
                    body, field = splitKey(key)
                    if body not in self.keys():
                        self.append(body, SurfaceGeometry(body))
                    self[body].append(field, Field(key, value))
                except IndexError:
                    self['GLOBAL'].append(key.lower(), Field(key, value))
            else:
                self['GLOBAL'].append(key.lower(), Field(key, value))

    def __repr__(self):
        return 'OPUS API list of all fields available ({}):\n'.format(len(self)) + \
               '\n'.join(' - {}'.format(key) for key in self)


class GlobalField(DataDict):
    def __init__(self):
        DataDict.__init__(self)
    
    def __repr__(self):
        return 'OPUS API Global fields ({}):\n'.format(len(self)) + \
                '\n'.join(' - {} ({})'.format(value, key) for key, value in self.items())


class SurfaceGeometry(GlobalField):
    def __init__(self, body):
        GlobalField.__init__(self)
        self.body = body
    
    def __repr__(self):
        return 'OPUS API Surface Geometry fields ({}) for `{}`:\n'.format(len(self), self.body.title()) + \
                '\n'.join(' - {} ({})'.format(value, key) for key, value in self.items())
