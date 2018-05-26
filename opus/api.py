# -*- coding: utf-8 -*-
import requests
import json

from .url import clean

API_URL = 'https://tools.pds-rings.seti.org/opus/api'

FMT = ['json', 'html', 'zip', 'csv']

class API(object):
    '''OPUS Seti Ring-Node API class'''

    def __init__(self, url=API_URL, verbose=False):
        self.url = clean(url)
        self.verbose = verbose

    def __str__(self):
        return self.url

    def __repr__(self):
        return "OPUS Seti Ring-Node API: {}".format(self.url)

    def request(self, entry, fmt='json', **kwargs):
        if fmt not in FMT:
            raise ValueError(
                "Format '{}' not in {}".format(fmt, FMT)
            )

        params = ''
        if len(kwargs) != 0:
            params = '?' + '&'.join(
                '{}={}'.format(key, value)
                for key, value in kwargs.items()
            )

        return self.url + entry + '.' + fmt + params

    def load(self, entry, **kwargs):
        url = self.request(entry, fmt='json', **kwargs)
        if self.verbose:
            print('Call to: {}'.format(url))

        response = requests.get(url)
        if(response.ok):
            return json.loads(response.content)
        else:
            raise RuntimeError('The OPUS API can not be reached')

    def count(self, **kwargs):
        '''Get result count for a search'''
        res = self.load('meta/result_count',  **kwargs)
        return int(res['data'][0]['result_count'])

    def data(self, limit=None, page=1, **kwargs):
        '''Get data for a search'''
        if limit is None:
            kwargs['limit'] = self.count(**kwargs)
        else:
            kwargs['limit'] = limit
            kwargs['page'] = page
        return self.load('data', **kwargs)
