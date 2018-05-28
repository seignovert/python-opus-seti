# -*- coding: utf-8 -*-

class Data(object):
    def __init__(self, json):
        self.json = json
        self.index = 0

    def __repr__(self):
        return 'OPUS API Data object (with {} elements)'.format(self.count)

    def __len__(self):
        return self.count

    def __getitem__(self, index):
        return self.json['page'][index]

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
        return int(self.json['count'])

    @property
    def limit(self):
        return int(self.json['limit'])

    @property
    def order(self):
        return self.json['order']

    @property
    def page_no(self):
        return int(self.json['page_no'])

    @property
    def labels(self):
        return self.json['labels']
