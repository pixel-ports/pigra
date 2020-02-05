#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, time, timezone

from pigra.sounding import Sounding, Location
from pigra.constants import P_SRC

sample = "#GRM00016622 2018 01 01 00 2333   72 ncdc-gts           405272   229714"

def test_header():
    sounding = Sounding(
        station="GRM00016622",
        obstime=datetime(2018, 1, 1, tzinfo=timezone.utc),
        reltime=time(23, 33),
        nlevels=72,
        datasource_p=P_SRC.ncdc_gts,
        datasource_np=None,
        location=Location(40.5272, 22.9714)
    )
    assert sounding.header() == "GRM00016622\t2018-01-01T00:00:00+00:00\t  72 levels"
