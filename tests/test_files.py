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


def test_file_meta(file_vims):
    assert 'OPUS API Files for observation: S_CUBE_CO_VIMS_1558621524_VIS' in repr(file_vims)
    assert str(file_vims) == 'S_CUBE_CO_VIMS_1558621524_VIS'
    assert file_vims.ring_obs_id == 'S_CUBE_CO_VIMS_1558621524_VIS'

def test_file_previews(file_iss):
    previews = file_iss['PREVIEWS']
    assert str(previews['full']) == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_full.jpg'
    assert str(previews['med']) == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_med.jpg'
    assert str(previews['small']) == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_small.jpg'
    assert str(previews['thumb']) == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_thumb.jpg'


def test_file_list_iss(file_iss):
    raw_image = file_iss['RAW_IMAGE']
    assert str(raw_image['LBL']) == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1.LBL'
    assert str(raw_image['IMG']) == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1.IMG'
    assert str(raw_image['tlmtab']) == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2001/LABEL/TLMTAB.FMT'
    assert str(raw_image['prefix2']) == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2001/LABEL/PREFIX2.FMT'

    calibrated = file_iss['CALIBRATED']
    assert str(calibrated['LBL']) == 'https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_CALIB.LBL'
    assert str(calibrated['IMG']) == 'https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_CALIB.IMG'
    assert str(calibrated['tlmtab']) == 'https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2001/LABEL/TLMTAB.FMT'
    assert str(calibrated['prefix2']) == 'https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2001/LABEL/PREFIX2.FMT'


def test_file_list_vims(file_vims):
    raw_spectral_image_cube = file_vims['RAW_SPECTRAL_IMAGE_CUBE']
    assert str(raw_spectral_image_cube['qub']) == 'https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/data/2007137T054828_2007143T180509/v1558621524_1.qub'
    assert str(raw_spectral_image_cube['QUB']) == 'https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/data/2007137T054828_2007143T180509/v1558621524_1.QUB'
    assert str(raw_spectral_image_cube['LBL']) == 'https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/data/2007137T054828_2007143T180509/v1558621524_1.LBL'
    assert str(raw_spectral_image_cube['suffix_description']) == 'https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/LABEL/suffix_description.fmt'
    assert str(raw_spectral_image_cube['core_description']) == 'https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/LABEL/core_description.fmt'
    assert str(raw_spectral_image_cube['band_bin_center']) == 'https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/LABEL/band_bin_center.fmt'
    

def test_files_meta(files):
    r = repr(files)
    assert 'OPUS API File objects (with 10 files)' in r
    assert 'S_CUBE_CO_VIMS_1558621524_VIS' in r
    assert len(files) == 10


def test_file_list_err():
    with pytest.raises(ValueError):
        FileList(['file.txt'])
