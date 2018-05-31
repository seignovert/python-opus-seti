# -*- coding: utf-8 -*-
import os
import requests
import shutil


class Downloadable(object):
    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return 'OPUS API downloadable file:\n -> {}'.format(str(self))

    def __str__(self):
        return self.url

    def download(self, out=None):
        outdir = None
        if out and os.path.isdir(out):
            outdir = out
            out = None

        if out is None:
            filename = self.url.split('/')[-1]
        else:
            filename = out

        if outdir:
            filename = os.path.join(outdir, filename)

        r = requests.get(self.url, stream=True)
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        return filename
