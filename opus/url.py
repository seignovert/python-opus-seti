# -*- coding: utf-8 -*-

def clean(url, pre='https://'):
    if '.' not in url and 'localhost' not in url:
        raise ValueError("Invalid url (no tld): {}".format(url))
    if len(url) < 4:
        raise ValueError("Invalid url (too short): {}".format(url))

    if not url.endswith('/'):
        url += '/'
    if url[:2] == '//':
        url = pre + url[2:]
    elif '://' not in url:
        url = pre + url

    return url
        
