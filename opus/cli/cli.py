# -*- coding: utf-8 -*-
import os
import argparse

from ..api import API

api = API()

def read(others):
    '''Extract optional arguments'''
    out = {}
    key = None
    for value in others:
        value = value.replace("'", '')
        if len(value) > 2:
            if value[:2] == '--':
                key = value[2:]
                value = None
                if '=' in key:
                    key, value = key.split('=', 1)
        if key and value:
            out[key] = value
            key = None
    return out


def data(argv=None, desc='Get Data from OPUS-SETI API', args=[], defaults={}, api=api):
    '''OPUS SETI API data entry point'''
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument('-a', '--all', action='store_true',
                        help='Get all the output at once (disable: --limit/--page)')
    parser.add_argument('-l', '--limit', default=10, type=int,
                        help='Output limits (default: 10)')
    parser.add_argument('-p', '--page', default=1, type=int,
                        help='Page offset (default: 1)')
    parser.add_argument('--field', help='Field key and value (sep. ` ` or `=`)', metavar='VALUE')

    for arg in args:
        for key, msg in arg.items():
            parser.add_argument(key, **msg)

    # Parse default args
    args, others = parser.parse_known_args(argv)

    # Set defaults optiona values
    for key, value in defaults.items():
        setattr(args, key, value)

    # Read other args
    for key, value in read(others).items():
        setattr(args, key, value)

    # Disble limit if flag `all` is present
    if args.all:
        setattr(args, 'limit', None)
        delattr(args, 'page')
    delattr(args, 'all')
    delattr(args, 'field')

    if args == argparse.Namespace(limit=10, page=1) or args == argparse.Namespace(limit=None):
        parser.print_help()
        os.sys.exit(2)

    return api.data(**vars(args))


def metadata(argv=None, api=api):
    '''OPUS SETI API metadata entry point'''
    parser = argparse.ArgumentParser(description='Get detail for a single observation from OPUS-SETI API')
    parser.add_argument('ring_obs_id', help='Valid ring_obs_id')
    args, others = parser.parse_known_args(argv)

    return api.metadata(args.ring_obs_id)

def image(argv=None, api=api):
    '''OPUS SETI API images/previews entry point'''
    parser = argparse.ArgumentParser(description='Get image for a single observation from OPUS-SETI API')
    parser.add_argument('ring_obs_id', help='Valid ring_obs_id')
    parser.add_argument('-s', '--size', help='Image size', default='med', choices=['thumb', 'small', 'med', 'full'])
    parser.add_argument('-d', '--download', help='Download the image', action='store_true')
    parser.add_argument('-o', '--output', help='Output folder/filename for download', default=None)
    args, others = parser.parse_known_args(argv)

    img = api.image(args.ring_obs_id, size=args.size)
    if args.download or args.output is not None:
        return img.download(out=args.output)
    return img.url

def files(argv=None, api=api):
    '''OPUS SETI API files entry point'''
    parser = argparse.ArgumentParser(description='Get files for a single observation from OPUS-SETI API')
    parser.add_argument('ring_obs_id', help='Valid ring_obs_id')
    parser.add_argument('-f', '--fmt', help='File format', default=None, nargs=2, metavar=('GROUP','FORMAT'))
    parser.add_argument('-d', '--download', help='Download the image', action='store_true')
    parser.add_argument('-o', '--output', help='Output folder/filename for download', default=None)
    args, others = parser.parse_known_args(argv)

    files = api.file(args.ring_obs_id)
    if args.fmt is not None:
        files = files[args.fmt[0]][args.fmt[1]]
        if args.download or args.output is not None:
            return files.download(out=args.output)
    return repr(files)

def field(argv=None, api=api):
    '''OPUS SETI API field entry point'''
    parser = argparse.ArgumentParser(description='Get information about field for OPUS-SETI API')
    parser.add_argument('field', help='Field name', nargs='?', metavar='name')
    parser.add_argument('--all', help='List all available fields', action='store_true')
    args, others = parser.parse_known_args(argv)

    if args.all:
        return api.fields()
    try:
        return api.field(args.field)
    except KeyError:
        try:
            return api.fields()[args.field]
        except KeyError:
            return 'Unknown field. To list all the available fields, run: `opus-field --all`'
