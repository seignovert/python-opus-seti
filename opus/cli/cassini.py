# -*- coding: utf-8 -*-

from ..api import API
from .cli import data

api = API()

def vims(argv=None, api=api):
    '''Cassini VIMS data entry point'''
    return data(argv, desc='Get Cassini VIMS Images and Cubes from OPUS API',
                args=[{'surfacegeometrytargetname': {'help': 'VIMS target name', 'metavar': 'TARGET_NAME'}},
                      {'--cols': {'default': 'ringobsid,target,revno,time1,primaryfilespec,channel',
                                  'help': 'Output columns (default: `ringobsid,target,revno,time1,primaryfilespec,channel`)'}}],
                defaults={'instrumentid': 'Cassini+VIMS', 'typeid': 'Image,Cube'}, api=api)
