# -*- coding: utf-8 -*-
import re

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
            return '`{}` -> {}\n{}\n_More info_: {}'.format(self.field, self.label, self.desc, self.url)
        else:
            return '`{}` -> {}'.format(self.field, self.label)

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


class Fields(object):
    def __init__(self, json):
        self._json = json
        self._data = {'GLOBAL': GlobalField()}
        for key, value in json.items():

            if 'surfacegeometry' in key:
                try:
                    body, field = splitKey(key)
                    if body not in self._data:
                        self._data[body] = SurfaceGeometry(body)
                    self._data[body].add(field, Field(key, value))
                except IndexError:
                    self._data['GLOBAL'].add(key.lower(), Field(key, value))
            else:
                self._data['GLOBAL'].add(key.lower(), Field(key, value))

    def __repr__(self):
        return 'OPUS API list of all fields ({})'.format(len(self))

    def __len__(self):
        return len(self._json)

    def __getitem__(self, attr):
        return self._data[attr.upper()]

    def __iter__(self):
        return iter(self._data)

    def keys(self):
        return self._data.keys()

    def items(self):
        return self._data.items()

    def values(self):
        return self._data.values()


class GlobalField(object):
    def __init__(self):
        self._fields = {}
    
    def __repr__(self):
        return 'OPUS API Global fields ({}):\n'.format(len(self)) + \
                '\n'.join(
                    ' - {} ({})'.format(value.label, key) for key, value in self.items()
                )

    def __len__(self):
        return len(self._fields)

    def __getitem__(self, attr):
        return self._fields[attr]

    def __iter__(self):
        return iter(self._fields)

    def keys(self):
        return self._fields.keys()

    def items(self):
        return self._fields.items()

    def values(self):
        return self._fields.values()

    def add(self, name, field):
        self._fields[name] = field

    def find(self, keyword):
        keyword = keyword.lower()
        keys = []
        for key, value in self.items():
            if keyword in value.label.lower():
                keys.append(key)
        if len(keys) == 0:
            return None
        return keys


class SurfaceGeometry(GlobalField):
    def __init__(self, body):
        GlobalField.__init__(self)
        self.body = body
    
    def __repr__(self):
        return 'OPUS API Surface Geometry fields ({}) for `{}`:\n'.format(len(self), self.body.title()) + \
                '\n'.join(
                    ' - {} ({})'.format(value.label, key) for key, value in self.items()
                )
