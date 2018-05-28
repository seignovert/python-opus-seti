# -*- coding: utf-8 -*-
import pytest
import responses
import json as JSON

from opus.images import *


@pytest.fixture
def size():
    return 'med'


@pytest.fixture
def json(size):
    return JSON.loads(open('tests/api/images/{}.json'.format(size), 'r').read())


@pytest.fixture
def images(json, size):
    return Images(json, size)


def test_images_meta(images, size):
    assert repr(images) == 'OPUS API Images object (with 10 images)'
    assert len(images) == 10
    assert images.order == 'obs_general.time1'
    assert images.size == size


def test_images_image(images):
    image = images[0]
    assert repr(image) == 'OPUS API Image object: S_IMG_CO_ISS_1508094647_N'
    assert str(image) == 'S_IMG_CO_ISS_1508094647_N'
    assert image.ring_obs_id == 'S_IMG_CO_ISS_1508094647_N'
    assert image.path == 'https://pds-rings.seti.org/holdings/previews/'
    assert image.img == 'COISS_2xxx/COISS_2016/data/1508054834_1508117267/N1508094647_1_med.jpg'
    assert image.url == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2016/data/1508054834_1508117267/N1508094647_1_med.jpg'
    

def test_images_iter(images):
    images.next() == images[0]
    for ii, img in enumerate(images):
        img = images[ii]
