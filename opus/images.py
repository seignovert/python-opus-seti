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
        self.json = json
        self.size = size
        self.index = 0

    def __repr__(self):
        return 'OPUS API Images object (with {} images)'.format(self.count)

    def __len__(self):
        return self.count

    def __getitem__(self, index):
        img = self.json['data'][index]
        return Image(img['ring_obs_id'], img['path'], img['img'])

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.__getitem__(self.index)
        except IndexError:
            self.index = 0
            raise StopIteration
        self.index += 1
        return result

    def next(self):
        return self.__next__()

    @property
    def count(self):
        return len(self.json['data'])

    @property
    def order(self):
        return self.json['order']
