# -*- coding: utf-8 -*-
import pytest
import os
import responses

from opus.wget import Downloadable


@pytest.fixture
def url():
    return 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_med.jpg'

@pytest.fixture
def downloadable(url):
    return Downloadable(url)


def test_downloadable(downloadable):
    assert downloadable.url in repr(downloadable)

@responses.activate
def test_download(downloadable):
    fname = 'N1459551972_1_med.jpg'
    with open('tests/api/image/med/'+fname, 'rb') as img:
        responses.add(responses.GET, downloadable.url,
                      body=img.read(), status=200,
                      content_type='image/jpeg',
                      stream=True
                      )

    downloadable.download(out='tests/')

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == downloadable.url

    assert os.path.isfile('tests/'+fname)
    os.remove('tests/'+fname)


@responses.activate
def test_download_output(downloadable):
    fname = 'N1459551972_1_med.jpg'
    with open('tests/api/image/med/'+fname, 'rb') as img:
        responses.add(responses.GET, downloadable.url,
                      body=img.read(), status=200,
                      content_type='image/jpeg',
                      stream=True
                      )

    downloadable.download(out='tests/test.jpg')

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == downloadable.url

    assert os.path.isfile('tests/test.jpg')
    os.remove('tests/test.jpg')
