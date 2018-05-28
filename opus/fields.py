# -*- coding: utf-8 -*-

class Field(object):
    def __init__(self, field, json):
        if len(json) == 0:
            raise KeyError('Unknown field `{}`'.format(field))

        self.field = field
        self.label = json[field]['label']
        self.definition = json[field]['more_info']['def'].replace('<br />','').replace('  ',' ')
        self.url = json[field]['more_info']['more_info']
        
    def __repr__(self):
        return '`{}` -> {}\n{}\n\nMore info: {}'.format(self.field, self.label, self.definition, self.url)
