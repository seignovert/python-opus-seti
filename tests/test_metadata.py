# -*- coding: utf-8 -*-
import pytest
import responses
import json as JSON

from opus.metadata import Metadata

@pytest.fixture
def json():
    return JSON.loads(open('tests/api/metadata/S_IMG_CO_ISS_1459551972_N.json', 'r').read())

@pytest.fixture
def metadata(json):
    return Metadata(json)


def test_metadata_repr(metadata):
    assert repr(metadata) == 'OPUS API Metadata Ring observation: S_IMG_CO_ISS_1459551972_N'


def test_metadata_general_constraints(metadata):
    assert metadata.is_image == True
    assert metadata.planet_id == 'SAT'
    assert metadata.target_name == 'SKY'
    assert metadata.mission_id == 'CO'
    assert metadata.inst_host_id == 'CO'
    assert metadata.instrument_id == 'COISS'
    assert metadata.time_sec1 == 134174599.095
    assert metadata.time_sec2 == 134174600.095
    assert metadata.target_class == 'SKY'
    assert metadata.quantity == 'REFLECT'
    assert metadata.type_id == 'IMG'
    assert metadata.ring_obs_id == 'S_IMG_CO_ISS_1459551972_N'
    assert metadata.right_asc1 == 66.998507
    assert metadata.right_asc2 == 67.400994
    assert metadata.declination1 == 15.826958
    assert metadata.declination2 == 16.213811
    assert metadata.observation_duration == 1.0
    assert metadata.volume_id_list == 'COISS_2001'
    assert metadata.primary_file_spec == 'COISS_2001/data/1459551663_1459568594/N1459551972_1.IMG'


# def test_metadata_time(metadata):
    # assert metadata.time1 == '2004-092T22:42:47.095'
    # assert metadata.time2 == '2004-092T22:42:48.095'


def test_metadata_err(metadata):
    with pytest.raises(AttributeError):
        metadata.note

    
