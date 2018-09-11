# -*- coding: utf-8 -*-
import pytest
import os
import responses
import json as JSON

from opus.images import Images, Image

@pytest.fixture
def size():
    return 'med'

@pytest.fixture
def images(size):
    json = JSON.loads(open('tests/api/images/{}.json'.format(size), 'r').read())
    return Images(json, size)

@pytest.fixture
def image(size):
    opus_id = 'COISS_2001-1459551663_1459568594-N1459551972_1'
    json = JSON.loads(open('tests/api/image/'+size+'/'+opus_id+'.json', 'r').read())
    return Image(opus_id, json['path'], json['data'][0]['img'])


def test_image(image):
    assert repr(image) == 'OPUS API Image object: COISS_2001-1459551663_1459568594-N1459551972_1'
    assert str(image) == 'COISS_2001-1459551663_1459568594-N1459551972_1'
    assert image.opus_id == 'COISS_2001-1459551663_1459568594-N1459551972_1'
    assert image.path == 'https://pds-rings.seti.org/holdings/previews/'
    assert image.img == 'COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_med.jpg'
    assert image.url == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_med.jpg'


def test_images_meta(images, size):
    r = repr(images)
    assert 'OPUS API Image objects' in r
    assert 'COISS_2016-1508054834_1508117267-N1508094647_1' in r
    assert len(images) == 10
    assert images.order == 'time1,opusid'
    assert images.size == size

