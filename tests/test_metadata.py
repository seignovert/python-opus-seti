# -*- coding: utf-8 -*-
import pytest

import json as JSON

from datetime import datetime as dt

from opus.metadata import *

@pytest.fixture
def json():
    return JSON.loads(open('tests/api/metadata/S_IMG_CO_ISS_1459551972_N.json', 'r').read())

@pytest.fixture
def metadata(json):
    return Metadata(json)


def test_read_time():
    assert read_time('2004-092T22:42:47.095') == dt(2004, 4, 1, 22, 42, 47, 95000)
    assert read_time('2004-04-01T22:42:47.095') == dt(2004, 4, 1, 22, 42, 47, 95000)

def test_read_time_err():
    with pytest.raises(ValueError):
        read_time('abc')


def test_metadata_repr(metadata):
    r = repr(metadata)
    assert 'OPUS API Metadata Ring observation: S_IMG_CO_ISS_1459551972_N' in r
    assert '=> GENERAL constraints' in r
    assert 'time1: 2004-04-01 22:42:47.095000' in r

def test_metadata_general_constraints(metadata):
    assert metadata['GENERAL']['is_image'] == True
    assert metadata['GENERAL']['planet_id'] == 'SAT'
    assert metadata['GENERAL']['target_name'] == 'SKY'
    assert metadata['GENERAL']['mission_id'] == 'CO'
    assert metadata['GENERAL']['inst_host_id'] == 'CO'
    assert metadata['GENERAL']['instrument_id'] == 'COISS'
    assert metadata['GENERAL']['time_sec1'] == 134174599.095
    assert metadata['GENERAL']['time_sec2'] == 134174600.095
    assert metadata['GENERAL']['time1'] == dt(2004, 4, 1, 22, 42, 47, 95000)
    assert metadata['GENERAL']['time2'] == dt(2004, 4, 1, 22, 42, 48, 95000)
    assert metadata['GENERAL']['target_class'] == 'SKY'
    assert metadata['GENERAL']['quantity'] == 'REFLECT'
    assert metadata['GENERAL']['type_id'] == 'IMG'
    assert metadata['GENERAL']['ring_obs_id'] == 'S_IMG_CO_ISS_1459551972_N'
    assert metadata['GENERAL']['right_asc1'] == 66.998507
    assert metadata['GENERAL']['right_asc2'] == 67.400994
    assert metadata['GENERAL']['declination1'] == 15.826958
    assert metadata['GENERAL']['declination2'] == 16.213811
    assert metadata['GENERAL']['observation_duration'] == 1.0
    assert metadata['GENERAL']['volume_id_list'] == 'COISS_2001'
    assert metadata['GENERAL']['primary_file_spec'] == 'COISS_2001/data/1459551663_1459568594/N1459551972_1.IMG'


def test_constraints_saturn_surface_geometry(metadata):
    constraints = metadata['SATURN_SURFACE_GEOMETRY']
    assert constraints['sub_solar_planetocentric_latitude'] == -25.081
    assert constraints['sub_observer_planetocentric_latitude'] == -16.319
    assert constraints['sub_solar_planetographic_latitude'] == -29.908
    assert constraints['sub_observer_planetographic_latitude'] == -19.79
    assert constraints['sub_solar_IAU_longitude'] == 35.936
    assert constraints['sub_observer_IAU_longitude'] == 106.634
    assert constraints['center_resolution'] == 268.851
    assert constraints['center_phase_angle'] == 66.02
    assert constraints['center_distance'] == 45067643.997
  

def test_constraints_ring_geometry(metadata):
    constraints = metadata['RING_GEOMETRY']
    assert constraints['ring_center_distance'] == 45067643.997
    assert constraints['sub_solar_ring_long'] == 286.798
    assert constraints['sub_observer_ring_long'] == 216.1
    assert constraints['ring_center_phase'] == 66.02
    assert constraints['ring_center_incidence'] == 64.919
    assert constraints['ring_center_emission'] == 73.682
    assert constraints['ring_center_north_based_incidence'] == 115.081
    assert constraints['ring_center_north_based_emission'] == 106.318
    assert constraints['solar_ring_opening_angle'] == -25.081
    assert constraints['observer_ring_opening_angle'] == -16.319


def test_constraints_wavelength(metadata):
    constraints = metadata['WAVELENGTH']
    assert constraints['wavelength1'] == 0.451
    assert constraints['wavelength2'] == 0.451
    assert constraints['spec_flag'] == 'N'
    assert constraints['polarization_type'] == 'NONE'
  

def test_constraints_image(metadata):
    constraints = metadata['IMAGE']
    assert constraints['duration'] == 1.0
    assert constraints['image_type_id'] == 'FRAM'
    assert constraints['greater_pixel_size'] == 1024.0
    assert constraints['lesser_pixel_size'] == 1024.0
    assert constraints['levels'] == '4096'

def test_constraints_cassini_mission(metadata):
    constraints = metadata['CASSINI_MISSION']
    assert constraints['cassini_target_name'] == 'instrument calibration'
    assert constraints['rev_no'] == 'C44'
    assert constraints['obs_name'] == 'ISS_C44IC_CALSTAR2001_PRIME'
    assert constraints['activity_name'] == 'CALSTAR2'
    assert constraints['spacecraft_clock_count1'] == 1459551971.131
    assert constraints['spacecraft_clock_count2'] == 1459551972.131
    assert constraints['prime'] == 'Y'
    assert constraints['prime_inst_id'] == 'COISS'
    assert constraints['ert_sec1'] == 134277636.336
    assert constraints['ert_sec2'] == 134277720.397
  

def test_constraints_cassini_iss(metadata):
    constraints = metadata['CASSINI_ISS']
    assert constraints['FILTER_NAME'] == 'BL1  ,CL2'
    assert constraints['INST_CMPRS_RATE_expected_average'] == 2.9
    assert constraints['INST_CMPRS_RATE_actual_average'] == 2.135712
    assert constraints['VALID_MAXIMUM_minimum_full_well_saturation_level'] == 4095
    assert constraints['VALID_MAXIMUM_maximum_DN_saturation_level'] == 4095
    assert constraints['ANTIBLOOMING_STATE_FLAG'] == 'ON'
    assert constraints['DELAYED_READOUT_FLAG'] == 'NO'
    assert constraints['FILTER_TEMPERATURE'] == -0.468354
    assert constraints['LIGHT_FLOOD_STATE_FLAG'] == 'ON'
    assert constraints['MISSING_PACKET_FLAG'] == 'NO'
    assert constraints['camera'] == 'N'
    assert constraints['FILTER'] == 'BL1'
    assert constraints['IMAGE_OBSERVATION_TYPE'] == 'CALIBRATION'
    assert constraints['SHUTTER_MODE_ID'] == 'NACONLY'
    assert constraints['DATA_CONVERSION_TYPE'] == '12BIT'
    assert constraints['GAIN_MODE_ID'] == '29 ELECTRONS PER DN'
    assert constraints['INST_CMPRS_TYPE'] == 'LOSSLESS'
    assert constraints['SHUTTER_STATE_ID'] == 'ENABLED'
    assert constraints['INST_CMPRS_RATIO'] == 7.491648
    assert constraints['TELEMETRY_FORMAT_ID'] == 'S_N_ER_3'
    assert constraints['MISSING_LINES'] == 0
    assert constraints['OPTICS_TEMPERATURE_front'] == 0.712693
    assert constraints['INST_CMPRS_PARAM_QF'] == -2147483648
    assert constraints['INST_CMPRS_PARAM_TB'] == -2147483648
    assert constraints['INST_CMPRS_PARAM_GOB'] == -2147483648
    assert constraints['EXPECTED_MAXIMUM_full_well_DN'] == 57.5369
    assert constraints['OPTICS_TEMPERATURE_rear'] == 1.905708
    assert constraints['EXPECTED_MAXIMUM_max_DN'] == 63.450699
    assert constraints['INST_CMPRS_PARAM_MALGO'] == -2147483648


def test_metadata_err(metadata):
    with pytest.raises(KeyError):
        metadata['FOO']

def test_constraints_err(metadata):
    with pytest.raises(KeyError):
        metadata['RING_GEOMETRY']['observer_ring_elevation2']
