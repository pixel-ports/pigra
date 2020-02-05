#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum


class P_SRC(Enum):
    bas_data = "bas-data"
    cdmp_amr = "cdmp-amr"
    cdmp_awc = "cdmp-awc"
    cdmp_mgr = "cdmp-mgr"
    cdmp_zdm = "cdmp-zdm"
    chuan101 = "chuan101"
    erac_hud = "erac-hud"
    iorgc_id = "iorgc-id"
    mfwa_ptu = "mfwa-ptu"
    ncar_ccd = "ncar-ccd"
    ncar_mit = "ncar-mit"
    ncdc6210 = "ncdc6210"
    ncdc6301 = "ncdc6301"
    ncdc6309 = "ncdc6309"
    ncdc6310 = "ncdc6310"
    ncdc6314 = "ncdc6314"
    ncdc6315 = "ncdc6315"
    ncdc6316 = "ncdc6316"
    ncdc6319 = "ncdc6319"
    ncdc6322 = "ncdc6322"
    ncdc6323 = "ncdc6323"
    ncdc6324 = "ncdc6324"
    ncdc6326 = "ncdc6326"
    ncdc6355 = "ncdc6355"
    ncdc_gts = "ncdc-gts"
    ncdc_nws = "ncdc-nws"
    ngdc_har = "ngdc-har"
    usaf_ds3 = "usaf-ds3"


class NP_SRC(Enum):
    cdmp_adp = "cdmp-adp"
    cdmp_awc = "cdmp-awc"
    cdmp_us2 = "cdmp-us2"
    cdmp_us3 = "cdmp-us3"
    cdmp_usm = "cdmp-usm"
    chuan101 = "chuan101"
    erac_hud = "erac-hud"
    mfwa_wnd = "mfwa-wnd"
    ncdc6301 = "ncdc6301"
    ncdc6309 = "ncdc6309"
    ncdc6314 = "ncdc6314"
    ncdc_gts = "ncdc-gts"
    ncdc_nws = "ncdc-nws"
    ngdc_har = "ngdc-har"
    usaf_ds3 = "usaf-ds3"


class LevelType:
    class Major(Enum):
        STANDARD = 1
        OTHER = 2
        NON = 3

    class Minor(Enum):
        OTHER = 0
        SURFACE = 1
        TROPOPAUSE = 2


class QualityFlag(Enum):
    UNCHECKED = " "  # Not checked by any climatology checks
    TIERS1 = "A"  # Value falls within "tier-1" climatological limits
    PASSED = "B"  # Quality Check Passed. Value passes checks based on both the tier-1 and tier-2
    REMOVED = "-8888"  # Value removed by IGRA quality assurance
    MISSING = "-9999"  # Value missing prior to quality assurance
    ERROR = "Z"  # Parsed value does not meet the specifications