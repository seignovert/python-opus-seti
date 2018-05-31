# -*- coding: utf-8 -*-

from .wget import download

class Image(object):
    def __init__(self, ring_obs_id, path, img):
        self.ring_obs_id = ring_obs_id
        self.path = path
        self.img = img

    def __repr__(self):
        return 'OPUS API Image object: {}'.format(self.ring_obs_id)

    def __str__(self):
        return self.ring_obs_id

    @property
    def url(self):
        return self.path + self.img

    def download(self, out=None):
        download(self.url, out)

class Images(object):
    def __init__(self, json, size):
        self._json = json
        self.size = size
        self._data = {}
        for img in json['data']:
            el = Image(img['ring_obs_id'], img['path'], img['img'])
            self._data[str(el)] = el

    def __repr__(self):
        return 'OPUS API Images object (with {} {} images):\n'.format(len(self), self.size) + \
               '\n'.join(' - {}'.format(key) for key, _ in self.items())

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


    @property
    def order(self):
        return self._json['order']
