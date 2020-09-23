# -*- coding: utf-8 -*-

from .data import DataDict
from .wget import Downloadable


class File(DataDict):
    '''Files for a single observation'''
    def __init__(self, opus_id, data):
        DataDict.__init__(self)
        self.opus_id = opus_id

        for label, files in data.items():
            if 'Browse Image' in label:
                value = Preview(files)
            else:
                value = FileList(files)
            key = label.replace('Browse Image ', '')\
                    .replace(' (calibrated unavailable)', '')\
                    .upper()\
                    .replace(' ', '_')\
                    .replace('(', '')\
                    .replace(')', '')

            self.append(key, value)

    def __repr__(self):
        return 'OPUS API Files for observation: {}\n'.format(self.opus_id) + \
               '\n'.join('\n=> {}\n{}'.format(key, value) for key, value in self.items())

    def __str__(self):
        return self.opus_id


class Preview(DataDict):
    '''Previews for a single observation'''
    def __init__(self, previews=[]):
        DataDict.__init__(self)
        for preview in previews:
            key = preview.split('_')[-1].split('.')[0]
            self.append(key, Downloadable(preview))

    def __repr__(self):
        return '\n'.join(' - {}: {}'.format(key, value) for key, value in self.items())

class FileList(DataDict):
    '''Files list for a single observation'''
    def __init__(self, files=[]):
        DataDict.__init__(self)
        for f in files:
            if f.lower().endswith('.lbl'):
                key = 'LBL'
            elif f.endswith('.IMG'):
                key = 'IMG'
            elif f.endswith('.qub'):
                key = 'qub'
            elif f.endswith('.tab'):
                key = 'TAB'
            elif f.endswith(('.jpg', '.jpeg', '.jpeg_small')):
                key = 'JPG'
            elif f.endswith('.png'):
                key = 'PNG'
            elif f.lower().endswith('.fmt'):
                key = f.lower().split('/')[-1].replace('.fmt', '')
            else:
                raise ValueError('Unknown file format `{}`'.format(f.lower().split('/')[-1]))

            self.append(key, Downloadable(f))

    def __repr__(self):
        return '\n'.join(' - {}: {}'.format(key, value) for key, value in self.items())


class Files(DataDict):
    def __init__(self, json):
        DataDict.__init__(self)
        self._json = json
        for key, value in json['data'].items():
            self.append(key, File(key, value))

    def __repr__(self):
        return 'OPUS API File objects (with {} files):\n'.format(len(self)) + \
               '\n'.join(' - {}'.format(key) for key in self.keys())
