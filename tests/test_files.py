# -*- coding: utf-8 -*-
import pytest

import json as JSON

from opus.files import *


@pytest.fixture
def files():
    json = JSON.loads(open('tests/api/files.json', 'r').read())
    return Files(json)

@pytest.fixture
def file_iss(files):
    json = JSON.loads(open('tests/api/files/S_IMG_CO_ISS_1459551972_N.json', 'r').read())
    return File('S_IMG_CO_ISS_1459551972_N', json['data']['S_IMG_CO_ISS_1459551972_N'])

@pytest.fixture
def file_vims(files):
    json = JSON.loads(open('tests/api/files/S_CUBE_CO_VIMS_1558621524_VIS.json', 'r').read())
    return File('S_CUBE_CO_VIMS_1558621524_VIS', json['data']['S_CUBE_CO_VIMS_1558621524_VIS'])


def test_files_meta(files):
    assert repr(files) == 'OPUS API Files object (with 10 files)'
    assert len(files) == 10

def test_files_iter(files):
    files.next() == files[0]
    for ii, img in enumerate(files):
        img = files[ii]

def test_file_meta(file_iss):
    assert repr(file_iss) == 'OPUS API Files for observation: S_IMG_CO_ISS_1459551972_N'
    assert str(file_iss) == 'S_IMG_CO_ISS_1459551972_N'
    assert file_iss.ring_obs_id == 'S_IMG_CO_ISS_1459551972_N'

def test_file_previews(file_iss):
    previews = file_iss.previews
    assert isinstance(repr(previews), str)
    assert previews.full == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_full.jpg'
    assert previews.med == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_med.jpg'
    assert previews.small == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_small.jpg'
    assert previews.thumb == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_thumb.jpg'


def test_file_list_iss(file_iss):
    raw_image = file_iss.raw_image
    assert raw_image.LBL == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1.LBL'
    assert raw_image.IMG == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1.IMG'
    assert raw_image.tlmtab == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2001/LABEL/TLMTAB.FMT'
    assert raw_image.prefix2 == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2001/LABEL/PREFIX2.FMT'

    calibrated = file_iss.calibrated
    assert calibrated.LBL == 'https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_CALIB.LBL'
    assert calibrated.IMG == 'https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_CALIB.IMG'
    assert calibrated.tlmtab == 'https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2001/LABEL/TLMTAB.FMT'
    assert calibrated.prefix2 == 'https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2001/LABEL/PREFIX2.FMT'


def test_file_list_vims(file_vims):
    assert isinstance(repr(file_vims.raw_spectral_image_cube), str)

def test_file_list_err():
    with pytest.raises(ValueError):
        FileList(['file.txt'])
