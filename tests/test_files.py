# -*- coding: utf-8 -*-
import pytest
import responses
import json as JSON

from opus.files import *


@pytest.fixture
def json():
    return JSON.loads(open('tests/api/files.json', 'r').read())


@pytest.fixture
def files(json):
    return Files(json)

@pytest.fixture
def ring_obs_file_iss(files):
   return files[2]

@pytest.fixture
def ring_obs_file_vims(files):
   return files[0]


def test_files_meta(files):
    assert repr(files) == 'OPUS API Files object (with 10 files)'
    assert len(files) == 10

def test_files_iter(files):
    files.next() == files[0]
    for ii, img in enumerate(files):
        img = files[ii]

def test_file_meta(ring_obs_file_iss):
    assert repr(ring_obs_file_iss) == 'OPUS API Files for observation: S_IMG_CO_ISS_1552517940_N'
    assert str(ring_obs_file_iss) == 'S_IMG_CO_ISS_1552517940_N'
    assert ring_obs_file_iss.ring_obs_id == 'S_IMG_CO_ISS_1552517940_N'

def test_file_previews(ring_obs_file_iss):
    previews = ring_obs_file_iss.previews
    assert repr(previews) == \
        'Full -> https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2030/data/1552434197_1552731724/N1552517940_1_full.jpg\n' + \
        'Med -> https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2030/data/1552434197_1552731724/N1552517940_1_med.jpg\n' + \
        'Small -> https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2030/data/1552434197_1552731724/N1552517940_1_small.jpg\n' + \
        'Thumb -> https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2030/data/1552434197_1552731724/N1552517940_1_thumb.jpg'

    assert previews.full == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2030/data/1552434197_1552731724/N1552517940_1_full.jpg'
    assert previews.med == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2030/data/1552434197_1552731724/N1552517940_1_med.jpg'
    assert previews.small == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2030/data/1552434197_1552731724/N1552517940_1_small.jpg'
    assert previews.thumb == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2030/data/1552434197_1552731724/N1552517940_1_thumb.jpg'


def test_file_list_iss(ring_obs_file_iss):
    raw_image = ring_obs_file_iss.raw_image
    assert raw_image.LBL == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2030/data/1552434197_1552731724/N1552517940_1.LBL'
    assert raw_image.IMG == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2030/data/1552434197_1552731724/N1552517940_1.IMG'
    assert raw_image.tlmtab == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2030/LABEL/TLMTAB.FMT'
    assert raw_image.prefix3 == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2030/LABEL/PREFIX3.FMT'

    calibrated = ring_obs_file_iss.calibrated
    assert calibrated.LBL == 'https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2030/data/1552434197_1552731724/N1552517940_1_CALIB.LBL'
    assert calibrated.IMG == 'https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2030/data/1552434197_1552731724/N1552517940_1_CALIB.IMG'
    assert calibrated.tlmtab == 'https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2030/LABEL/TLMTAB.FMT'
    assert calibrated.prefix3 == 'https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2030/LABEL/PREFIX3.FMT'


def test_file_list_vims(ring_obs_file_vims):
    assert repr(ring_obs_file_vims.raw_spectral_image_cube) == \
        'qub -> https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/data/2007137T054828_2007143T180509/v1558621524_1.qub\n' + \
        'QUB -> https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/data/2007137T054828_2007143T180509/v1558621524_1.QUB\n' + \
        'LBL -> https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/data/2007137T054828_2007143T180509/v1558621524_1.LBL\n' + \
        'suffix_description -> https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/LABEL/suffix_description.fmt\n' + \
        'core_description -> https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/LABEL/core_description.fmt\n' + \
        'band_bin_center -> https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/LABEL/band_bin_center.fmt'

def test_file_list_err():
    with pytest.raises(ValueError):
        FileList(['file.txt'])
