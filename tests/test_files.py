# -*- coding: utf-8 -*-
import pytest

import json as JSON

from opus.files import *


@pytest.fixture
def files():
    json = JSON.loads(open('tests/api/files.json', 'r').read())
    return Files(json)

@pytest.fixture
def file_iss_old(files):
    json = JSON.loads(open('tests/api/files/COISS_2001-1459551663_1459568594-N1459551972_1.json', 'r').read())
    return File('COISS_2001-1459551663_1459568594-N1459551972_1', json['data']['COISS_2001-1459551663_1459568594-N1459551972_1'])

@pytest.fixture
def file_iss(files):
    json = JSON.loads(open('tests/api/files/co-iss-n1487299402.json', 'r').read())
    return File('co-iss-n1487299402', json['data']['co-iss-n1487299402'])

@pytest.fixture
def file_vims(files):
    json = JSON.loads(open('tests/api/files/COVIMS_0020-2007137T054828_2007143T180509-v1558621524_1_VIS.json', 'r').read())
    return File('COVIMS_0020-2007137T054828_2007143T180509-v1558621524_1_VIS', json['data']['COVIMS_0020-2007137T054828_2007143T180509-v1558621524_1_VIS'])

@pytest.fixture
def file_galileo(files):
    json = JSON.loads(open('tests/api/files/go-ssi-c0349875100.json', 'r').read())
    return File('go-ssi-c0349875100', json['data']['go-ssi-c0349875100'])


def test_file_meta(file_vims):
    assert 'OPUS API Files for observation: COVIMS_0020-2007137T054828_2007143T180509-v1558621524_1_VIS' in repr(file_vims)
    assert str(file_vims) == 'COVIMS_0020-2007137T054828_2007143T180509-v1558621524_1_VIS'
    assert file_vims.opus_id == 'COVIMS_0020-2007137T054828_2007143T180509-v1558621524_1_VIS'

def test_file_previews(file_iss_old):
    previews = file_iss_old['FULL-SIZE']
    assert str(previews['full']) == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_full.jpg'

def test_file_list_iss_old(file_iss_old):
    raw_image = file_iss_old['RAW_DATA']
    assert str(raw_image['LBL']) == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1.LBL'
    assert str(raw_image['IMG']) == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1.IMG'
    assert str(raw_image['prefix2']) == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2001/label/prefix2.fmt'
    assert str(raw_image['tlmtab']) == 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2001/label/tlmtab.fmt'

    calibrated = file_iss_old['CALIBRATED_DATA']
    assert str(calibrated['IMG']) == 'https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_CALIB.IMG'
    assert str(calibrated['LBL']) == 'https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_CALIB.LBL'


def test_file_list_iss(file_iss):
    raw_image = file_iss['COISS_RAW']
    assert str(raw_image['IMG']) == 'https://opus.pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2009/data/1487182149_1487415680/N1487299402_1.IMG'
    assert str(raw_image['LBL']) == 'https://opus.pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2009/data/1487182149_1487415680/N1487299402_1.LBL'
    assert str(raw_image['prefix2']) == 'https://opus.pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2009/label/prefix2.fmt'
    assert str(raw_image['tlmtab']) == 'https://opus.pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2009/label/tlmtab.fmt'

    calibrated = file_iss['COISS_CALIB']
    assert str(calibrated['IMG']) == 'https://opus.pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2009/data/1487182149_1487415680/N1487299402_1_CALIB.IMG'
    assert str(calibrated['LBL']) == 'https://opus.pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2009/data/1487182149_1487415680/N1487299402_1_CALIB.LBL'

    thumb = file_iss['COISS_THUMB']
    assert str(thumb['JPG']) == 'https://opus.pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2009/extras/thumbnail/1487182149_1487415680/N1487299402_1.IMG.jpeg_small'

    full = file_iss['COISS_FULL']
    assert str(full['PNG']) == 'https://opus.pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2009/extras/full/1487182149_1487415680/N1487299402_1.IMG.png'


def test_file_list_vims(file_vims):
    raw_spectral_image_cube = file_vims['RAW_DATA']
    assert str(raw_spectral_image_cube['qub']) == 'https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/data/2007137T054828_2007143T180509/v1558621524_1.qub'
    assert str(raw_spectral_image_cube['LBL']) == 'https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/data/2007137T054828_2007143T180509/v1558621524_1.lbl'
    assert str(raw_spectral_image_cube['band_bin_center']) == 'https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/label/band_bin_center.fmt'
    assert str(raw_spectral_image_cube['core_description']) == 'https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/label/core_description.fmt'
    assert str(raw_spectral_image_cube['suffix_description']) == 'https://pds-rings.seti.org/holdings/volumes/COVIMS_0xxx/COVIMS_0020/label/suffix_description.fmt'


def test_file_list_galileo(file_galileo):
    raw_image = file_galileo['GOSSI_RAW']
    assert str(raw_image['IMG']) == 'https://opus.pds-rings.seti.org/holdings/volumes/GO_0xxx/GO_0017/G1/EUROPA/C0349875100R.IMG'
    assert str(raw_image['LBL']) == 'https://opus.pds-rings.seti.org/holdings/volumes/GO_0xxx/GO_0017/G1/EUROPA/C0349875100R.LBL'
    assert str(raw_image['rlineprx']) == 'https://opus.pds-rings.seti.org/holdings/volumes/GO_0xxx/GO_0017/LABEL/RLINEPRX.FMT'
    assert str(raw_image['rtlmtab']) == 'https://opus.pds-rings.seti.org/holdings/volumes/GO_0xxx/GO_0017/LABEL/RTLMTAB.FMT'

    thumb_image = file_galileo['BROWSE_THUMB']
    assert str(thumb_image['JPG']) == 'https://opus.pds-rings.seti.org/holdings/previews/GO_0xxx/GO_0017/G1/EUROPA/C0349875100R_thumb.jpg'


def test_files_meta(files):
    r = repr(files)
    assert 'OPUS API File objects (with 10 files)' in r
    assert 'COISS_2016-1508054834_1508117267-N1508094647_1' in r
    assert len(files) == 10


def test_file_list_err():
    with pytest.raises(ValueError):
        FileList(['file.txt'])
