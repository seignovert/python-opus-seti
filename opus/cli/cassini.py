# -*- coding: utf-8 -*-

from ..api import API
from .cli import data

api = API()

def vims(argv=None, api=api):
    '''Cassini VIMS data entry point'''
    return data(argv, desc='Get Cassini VIMS Images and Cubes from OPUS API',
                args=[{'target': {'help': 'VIMS target name', 'metavar': 'TARGET_NAME'}},
                      {'--cols': {'default': 'opusid,target,revno,time1,primaryfilespec',
                                  'help': 'Output columns (default: `opusid,target,revno,time1,primaryfilespec`)'}}],
                defaults={'instrumentid': 'Cassini+VIMS', 'COVIMSswathlength1': 2, 'COVIMSswathwidth1': 2}, api=api)
