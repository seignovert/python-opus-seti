# -*- coding: utf-8 -*-
import pytest
import json as JSON
from datetime import datetime as dt

from opus.metadata import *

@pytest.fixture
def json():
    return JSON.loads(open('tests/api/metadata_v2/COISS_2001-1459551663_1459568594-N1459551972_1.json', 'r').read())

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
    assert 'OPUS API Metadata Ring observation: COISS_2001-1459551663_1459568594-N1459551972_1' in r
    assert '=> GENERAL constraints' in r
    assert 'time1: 2004-04-01 22:42:47.095000' in r

def test_metadata_general_constraints(metadata):
    constraints = metadata['GENERAL']
    assert constraints['planet'] == "Saturn"
    assert constraints['target'] == "Sky"
    assert constraints['targetclass'] == "Sky"
    assert constraints['mission'] == "Cassini"
    assert constraints['insthost'] == "Cassini"
    assert constraints['instrument'] == "Cassini ISS"
    assert constraints['time1'] == dt(2004, 4, 1, 22, 42, 47, 95000)
    assert constraints['time2'] == dt(2004, 4, 1, 22, 42, 48, 95000)
    assert constraints['timesec1'] == 134174599.095
    assert constraints['timesec2'] == 134174600.095
    assert constraints['observationduration'] == 1.0
    assert constraints['spatialsampling'] == "2-D"
    assert constraints['wavelengthsampling'] == "No"
    assert constraints['quantity'] == "Reflectivity"
    assert constraints['rightasc1'] == 66.998507
    assert constraints['rightasc2'] == 67.400994
    assert constraints['declination1'] == 15.826958
    assert constraints['declination2'] == 16.213811
    assert constraints['opusid'] == "COISS_2001-1459551663_1459568594-N1459551972_1"
    assert constraints['ringobsid'] == "S_IMG_CO_ISS_1459551972_N"

def test_pds_constraints(metadata):
    constraints = metadata['PDS']
    assert constraints['volumeid'] == "COISS_2001"
    assert constraints['datasetid'] == "CO-S-ISSNA/ISSWA-2-EDR-V1.0"
    assert constraints['productid'] == "1_N1459551972.131"
    assert constraints['productcreationtime'] == dt(2004, 4, 3, 20, 9, 2)
    assert constraints['productcreationtimesec'] == 134338174.0
    assert constraints['primaryfilespec'] == "COISS_2001/data/1459551663_1459568594/N1459551972_1.IMG"

def test_image_constraints_ring_geometry(metadata):
    constraints = metadata['IMAGE']
    assert constraints['duration'] == 1.0
    assert constraints['greaterpixelsize'] == 1024
    assert constraints['lesserpixelsize'] == 1024
    assert constraints['levels'] == 4096
    assert constraints['imagetype'] == "Frame"

def test_wavelength_constraints(metadata):
    constraints = metadata['WAVELENGTH']
    assert constraints['wavelength1'] == 0.399353
    assert constraints['wavelength2'] == 0.502349
    assert constraints['waveres1'] == 0.10299599999999992
    assert constraints['waveres2'] == 0.10299599999999992
    assert constraints['waveno1'] == 19906.479359966877
    assert constraints['waveno2'] == 25040.503013624537
    assert constraints['wavenores1'] == 5134.023653657659
    assert constraints['wavenores2'] == 5134.023653657659
    assert constraints['specflag'] == "No"
    assert constraints['polarizationtype'] == "None"

def test_saturn_surface_geometry_constraints(metadata):
    constraints = metadata['SATURN_SURFACE_GEOMETRY']
    assert constraints['SURFACEGEOsaturnsubsolarplanetographiclatitude'] == -29.908
    assert constraints['SURFACEGEOsaturnsubobserverplanetographiclatitude'] == -19.79
    assert constraints['SURFACEGEOsaturnsubsolarplanetocentriclatitude'] == -25.081
    assert constraints['SURFACEGEOsaturnsubobserverplanetocentriclatitude'] == -16.319
    assert constraints['SURFACEGEOsaturnsubsolarIAUlongitude'] == 35.936
    assert constraints['SURFACEGEOsaturnsubobserverIAUlongitude'] == 106.634
    assert constraints['SURFACEGEOsaturncenterdistance'] == 45067643.997
    assert constraints['SURFACEGEOsaturncenterresolution'] == 268.851
    assert constraints['SURFACEGEOsaturncenterphaseangle'] == 66.02

def test_ring_geometry_constraints(metadata):
    constraints = metadata['RING_GEOMETRY']
    assert constraints['RINGGEOsubsolarringlong'] == 286.798
    assert constraints['RINGGEOsubobserverringlong'] == 216.1
    assert constraints['RINGGEOringcenterdistance'] == 45067643.997
    assert constraints['RINGGEOringcenterphase'] == 66.02
    assert constraints['RINGGEOringcenterincidence'] == 64.919
    assert constraints['RINGGEOringcenteremission'] == 73.682
    assert constraints['RINGGEOringcenternorthbasedincidence'] == 115.081
    assert constraints['RINGGEOringcenternorthbasedemission'] == 106.318
    assert constraints['RINGGEOsolarringopeningangle'] == -25.081
    assert constraints['RINGGEOobserverringopeningangle'] == -16.319

def test_cassini_mission_constraints(metadata):
    constraints = metadata['CASSINI_MISSION']
    assert constraints['CASSINIobsname'] == "ISS_C44IC_CALSTAR2001_PRIME"
    assert constraints['CASSINIactivityname'] == "CALSTAR2"
    assert constraints['CASSINImissionphasename'] == "Approach Science"
    assert constraints['CASSINItargetcode'] == "IC (Instrument calibration)"
    assert constraints['CASSINIrevno'] == "NULL"
    assert constraints['CASSINIprimeinst'] == "ISS"
    assert constraints['CASSINIisprime'] == "Yes"
    assert constraints['CASSINIsequenceid'] == "C44"
    assert constraints['CASSINIspacecraftclockcount1'] == "1/1459551971.131"
    assert constraints['CASSINIspacecraftclockcount2'] == "1/1459551972.131"
    assert constraints['CASSINIspacecraftclockcountdec1'] == 1459551971.5117188
    assert constraints['CASSINIspacecraftclockcountdec2'] == 1459551972.5117188
    assert constraints['CASSINIert1'] == "2004-094T15:20:04.336"
    assert constraints['CASSINIert2'] == "2004-094T15:21:28.397"
    assert constraints['CASSINIertsec1'] == 134320836.336
    assert constraints['CASSINIertsec2'] == 134320920.397

def test_cassini_iss_constraints(metadata):
    constraints = metadata['CASSINI_ISS']
    assert constraints['COISScamera'] == "Narrow Angle"
    assert constraints['COISSfilter'] == "BL1"
    assert constraints['COISSshuttermode'] == "NACONLY"
    assert constraints['COISSshutterstate'] == "Enabled"
    assert constraints['COISScompressiontype'] == "Lossless"
    assert constraints['COISSdataconversiontype'] == "12BIT"
    assert constraints['COISSgainmode'] == "29 Electrons per DN"
    assert constraints['COISSinstrumentmode'] == "FULL"
    assert constraints['COISSmissinglines'] == 0
    assert constraints['COISSimagenumber'] == 1459551972
    assert constraints['COISStargetdesc'] == "STAR"
    assert constraints['COISSimageobservationtype'] == "Calibration"

def test_metadata_err(metadata):
    with pytest.raises(KeyError):
        metadata['FOO']

def test_constraints_err(metadata):
    with pytest.raises(KeyError):
        metadata['RING_GEOMETRY']['observer_ring_elevation2']
