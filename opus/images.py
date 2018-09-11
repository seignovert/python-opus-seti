# -*- coding: utf-8 -*-

from .data import DataDict
from .wget import Downloadable


class Image(Downloadable):
    def __init__(self, opus_id, path, img):
        Downloadable.__init__(self, path + img)
        self.opus_id = opus_id
        self.path = path
        self.img = img

    def __repr__(self):
        return 'OPUS API Image object: {}'.format(self.opus_id)

    def __str__(self):
        return self.opus_id


class Images(DataDict):
    def __init__(self, json, size):
        DataDict.__init__(self)
        self._json = json
        self.size = size
        for img in json['data']:
            el = Image(img['opus_id'], img['path'], img['img'])
            self._data[str(el)] = el

    def __repr__(self):
        return 'OPUS API Image objects (with {} {} images):\n'.format(len(self), self.size) + \
               '\n'.join(' - {}'.format(key) for key, _ in self.items())

    @property
    def order(self):
        return self._json['order']
