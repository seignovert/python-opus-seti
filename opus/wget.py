# -*- coding: utf-8 -*-
import os
import requests
import shutil

def download(url, out=None):
    outdir = None
    if out and os.path.isdir(out):
        outdir = out
        out = None

    if out is None:
        filename = url.split('/')[-1]
    else:
        filename = out

    if outdir:
        filename = os.path.join(outdir, filename)

    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    return filename
