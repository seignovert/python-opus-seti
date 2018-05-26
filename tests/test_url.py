import pytest

from opus.url import *

def test_clean():
    url_http = 'http://example.tld/'
    url_https = 'https://example.tld/'
    url_slash = 'https://example.tld'
    url_dslash = '//example.tld'
    url_short = 'example.tld'
    assert clean(url_http) == url_http
    assert clean(url_https) == url_https
    assert clean(url_slash) == url_https
    assert clean(url_dslash) == url_https
    assert clean(url_short) == url_https


def test_clean_err():
    with pytest.raises(ValueError):
        clean('abc')
    with pytest.raises(ValueError):
        clean('a.b')
