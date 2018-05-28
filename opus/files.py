# -*- coding: utf-8 -*-

class File(object):
    '''Files for a single observation'''
    def __init__(self, ring_obs_id, data):
        self.ring_obs_id = ring_obs_id
        self._data = data
        
        for label, files in self._data.items():
            if label == 'preview_image':
                key = 'previews'
                value = Preview(files)
            else:
                key = label.lower()
                value = FileList(files)

            setattr(self, key, value)

    def __repr__(self):
        return 'OPUS API Files for observation: {}'.format(self.ring_obs_id)

    def __str__(self):
        return self.ring_obs_id

class Preview(object):
    '''Previews for a single observation'''
    def __init__(self, previews=[]):
        for preview in previews:
            key = preview.split('_')[-1].replace('.jpg', '').replace('.png','')
            setattr(self, key, preview)

    def __repr__(self):
        return '\n'.join(
            ['{} -> {}'.format(key.title(), value)
            for key, value in self.__dict__.items()]
        )

class FileList(object):
    '''Files list for a single observation'''
    def __init__(self, files=[]):
        for f in files:
            if f.endswith('.LBL'):
                key = 'LBL'
            elif f.endswith('.IMG'):
                key = 'IMG'
            elif f.endswith('.qub'):
                key = 'qub'
            elif f.endswith('.QUB'):
                key = 'QUB'
            elif f.lower().endswith('.fmt'):
                key = f.lower().split('/')[-1].replace('.fmt', '')
            else:
                raise ValueError('Unknown file format `{}`'.format(f.lower().split('/')[-1]))

            setattr(self, key, f)

    def __repr__(self):
        return '\n'.join(
            ['{} -> {}'.format(key, value)
            for key, value in self.__dict__.items()]
        )


class Files(object):
    def __init__(self, json):
        self.json = json
        self.imgs = list(self.json['data'].keys())
        self.index = 0

    def __repr__(self):
        return 'OPUS API Files object (with {} files)'.format(self.count)

    def __len__(self):
        return self.count

    def __getitem__(self, index):
        ring_obs_id = self.imgs[index]
        data = self.json['data'][ring_obs_id]
        return File(ring_obs_id, data)

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
