#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import pkg_resources

from datetime import datetime, time, timezone

from pigra.parser import IgraParser, SoundingException
from pigra.sounding import Sounding, Location
from pigra.constants import P_SRC, LevelType, QualityFlag
from pigra.utils import stream_from

igra_sample = [
    """#GRM00016622 2018 01 01 00 2333    2 ncdc-gts           405272   229714
21 -9999 102000B-9999    30B-9999    50   120    21
20 -9999 101600A-9999    66B-9999    60 -9999 -9999
""",
    """#GRM00016622 2018 01 01 00 2333    2 ncdc-gts           405272   229714
21 -9999 102000B-9999    30B-9999    50   120    21
20 -9999 101600A-9999    66B-9999    60 -9999 -9999
#GRM00016622 2018 01 02 00 2310    3 ncdc-gts           405272   229714
21 -9999 101300B-9999    46B-9999    39   120    15
20 -9999 101000 -9999    74B-9999    31 -9999 -9999
20 -9999 100700 -9999    82B-9999    39 -9999 -9999
"""
]


def test_header_success_1():
    header = "#GRM00016622 2018 01 01 00 2333    2 ncdc-gts           405272   229714"
    expected = Sounding(
        station="GRM00016622",
        obstime=datetime(2018, 1, 1, 0, 0, tzinfo=timezone.utc),
        reltime=time(23, 33),
        nlevels=2,
        datasource_p=P_SRC.ncdc_gts,
        datasource_np=None,
        location=Location(40.5272, 22.9714)
    )
    sounding = IgraParser.parse_header(header)
    assert sounding == expected


def test_header_success_2():
    header = "#GRM00016622 2018 01 02 00 2310    3 ncdc-gts           405272   229714"
    expected = Sounding(
        station="GRM00016622",
        obstime=datetime(2018, 1, 2, 0, 0, tzinfo=timezone.utc),
        reltime=time(23, 10),
        nlevels=3,
        datasource_p=P_SRC.ncdc_gts,
        datasource_np=None,
        location=Location(40.5272, 22.9714)
    )
    sounding = IgraParser.parse_header(header)
    assert sounding == expected


def test_header_success_missing_observation_time_hour():
    header = "#GRM00016622 2018 01 01 99 2333    2 ncdc-gts           405272   229714"
    expected = Sounding(
        station="GRM00016622",
        obstime=datetime(2018, 1, 1, 0, 0, tzinfo=timezone.utc),
        reltime=time(23, 33),
        nlevels=2,
        datasource_p=P_SRC.ncdc_gts,
        datasource_np=None,
        location=Location(40.5272, 22.9714)
    )
    sounding = IgraParser.parse_header(header)
    assert sounding == expected


def test_header_success_missing_release_time_minute():
    header = "#GRM00016622 2018 01 01 00 2399    2 ncdc-gts           405272   229714"
    expected = Sounding(
        station="GRM00016622",
        obstime=datetime(2018, 1, 1, 0, 0, tzinfo=timezone.utc),
        reltime=time(23),
        nlevels=2,
        datasource_p=P_SRC.ncdc_gts,
        datasource_np=None,
        location=Location(40.5272, 22.9714)
    )
    sounding = IgraParser.parse_header(header)
    assert sounding == expected


def test_header_success_missing_release_time():
    header = "#GRM00016622 2018 01 01 00 9999    2 ncdc-gts           405272   229714"
    expected = Sounding(
        station="GRM00016622",
        obstime=datetime(2018, 1, 1, 0, 0, tzinfo=timezone.utc),
        reltime=None,
        nlevels=2,
        datasource_p=P_SRC.ncdc_gts,
        datasource_np=None,
        location=Location(40.5272, 22.9714)
    )
    sounding = IgraParser.parse_header(header)
    assert sounding == expected


def test_header_bad_headrec():
    header = "?GRM00016622 2018 01 01 00 2333    2 ncdc-gts           405272   229714"
    with pytest.raises(SoundingException, match=r".*character.*"):
        IgraParser.parse_header(header)


def test_header_bad_length():
    header = "#GRM00016622 2018 01 01 00 2333    2 ncdc-gts           405272   229714P"
    with pytest.raises(SoundingException, match=r".*length.*"):
        IgraParser.parse_header(header)


def test_level_success_1_1():
    line = "21 -9999 102000B-9999    30B-9999    50   120    21"
    expected = Sounding.Level(
        major=LevelType.Major.OTHER,
        minor=LevelType.Minor.SURFACE,
        elapsed=(None, QualityFlag.MISSING),
        pressure=(102000, QualityFlag.PASSED),
        height=(None, QualityFlag.UNCHECKED),
        temperature=(3.0, QualityFlag.PASSED),
        humidity=(None, QualityFlag.MISSING),
        dewpoint=(5.0, QualityFlag.PASSED),
        winddir=(120, QualityFlag.PASSED),
        windspeed=(2.1, QualityFlag.PASSED)
    )
    level = IgraParser.parse_level(line)
    assert level == expected


def test_level_success_1_2():
    line = "20 -9999 101600A-9999    66B-9999    60 -9999 -9999"
    expected = Sounding.Level(
        major=LevelType.Major.OTHER,
        minor=LevelType.Minor.OTHER,
        elapsed=(None, QualityFlag.MISSING),
        pressure=(101600, QualityFlag.TIERS1),
        height=(None, QualityFlag.UNCHECKED),
        temperature=(6.6, QualityFlag.PASSED),
        humidity=(None, QualityFlag.MISSING),
        dewpoint=(6.0, QualityFlag.PASSED),
        winddir=(None, QualityFlag.MISSING),
        windspeed=(None, QualityFlag.MISSING)
    )
    level = IgraParser.parse_level(line)
    assert level == expected


def test_level_success_2_1():
    line = "21 -9999 101300B-9999    46B-9999    39   120    15"
    expected = Sounding.Level(
        major=LevelType.Major.OTHER,
        minor=LevelType.Minor.SURFACE,
        elapsed=(None, QualityFlag.MISSING),
        pressure=(101300, QualityFlag.PASSED),
        height=(None, QualityFlag.UNCHECKED),
        temperature=(4.6, QualityFlag.PASSED),
        humidity=(None, QualityFlag.MISSING),
        dewpoint=(3.9, QualityFlag.PASSED),
        winddir=(120, QualityFlag.PASSED),
        windspeed=(1.5, QualityFlag.PASSED)
    )
    level = IgraParser.parse_level(line)
    assert level == expected


def test_level_success_2_2():
    line = "20 -9999 101000 -9999    74B-9999    31 -9999 -9999"
    expected = Sounding.Level(
        major=LevelType.Major.OTHER,
        minor=LevelType.Minor.OTHER,
        elapsed=(None, QualityFlag.MISSING),
        pressure=(101000, QualityFlag.UNCHECKED),
        height=(None, QualityFlag.UNCHECKED),
        temperature=(7.4, QualityFlag.PASSED),
        humidity=(None, QualityFlag.MISSING),
        dewpoint=(3.1, QualityFlag.PASSED),
        winddir=(None, QualityFlag.MISSING),
        windspeed=(None, QualityFlag.MISSING)
    )
    level = IgraParser.parse_level(line)
    assert level == expected


def test_level_success_2_3():
    line = "20 -9999 100700 -9999    82B-9999    39 -9999 -9999"
    expected = Sounding.Level(
        major=LevelType.Major.OTHER,
        minor=LevelType.Minor.OTHER,
        elapsed=(None, QualityFlag.MISSING),
        pressure=(100700, QualityFlag.UNCHECKED),
        height=(None, QualityFlag.UNCHECKED),
        temperature=(8.2, QualityFlag.PASSED),
        humidity=(None, QualityFlag.MISSING),
        dewpoint=(3.9, QualityFlag.PASSED),
        winddir=(None, QualityFlag.MISSING),
        windspeed=(None, QualityFlag.MISSING)
    )
    level = IgraParser.parse_level(line)
    assert level == expected


def test_sample0():
    stream = igra_sample[0].split("\n")
    stream.remove("")
    parser = IgraParser(stream)
    soundings = [x for x in parser.parse()]
    assert len(soundings) == 1
    sounding = soundings[0]
    assert len(sounding.levels) == 2
    assert parser.stats == IgraParser.Stats(lines=3, null=0, records=1, processed=1, filtered=0, errors=0, warnings=0)


def test_sample1():
    stream = igra_sample[1].split("\n")
    stream.remove("")
    parser = IgraParser(stream)
    soundings = [x for x in parser.parse()]
    assert len(soundings) == 2
    sounding = soundings[0]
    assert len(sounding.levels) == 2
    sounding = soundings[1]
    assert len(sounding.levels) == 3
    assert parser.stats == IgraParser.Stats(lines=7, null=0, records=2, processed=2, filtered=0, errors=0, warnings=0)

def test_complete_file():
    filename = pkg_resources.resource_filename(__name__, "data/GRM00016622-data.txt.zip")
    stream = stream_from(filename)
    parser = IgraParser(stream)
    parser.analyze()    
    assert parser.stats == IgraParser.Stats(lines=1152034, null=0, records=25801, processed=25801, filtered=0, errors=0, warnings=277)
