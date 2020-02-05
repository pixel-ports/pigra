#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime, timedelta, time
from typing import List, Optional, Tuple

from pigra.constants import P_SRC, NP_SRC, LevelType, QualityFlag


@dataclass
class Location:
    lat: float = 0.0
    lon: float = 0.0
    
    @property
    def __geo_interface__(self):
        return {'type': 'Point', 'coordinates': (self.lon, self.lat)}

    def __iter__(self):
        return (self.lon, self.lat).__iter__()


@dataclass
class Sounding:

    @dataclass
    class Level:
        major: LevelType.Major
        minor: LevelType.Minor
        elapsed: Tuple[Optional[timedelta], QualityFlag]
        pressure: Tuple[Optional[int], QualityFlag]
        height: Tuple[Optional[int], QualityFlag]
        temperature: Tuple[Optional[float], QualityFlag]
        humidity: Tuple[Optional[float], QualityFlag]
        dewpoint: Tuple[Optional[float], QualityFlag]
        winddir: Tuple[Optional[int], QualityFlag]
        windspeed: Tuple[Optional[float], QualityFlag]

    station: str
    obstime: datetime
    reltime: Optional[time]
    nlevels: int
    datasource_p: Optional[P_SRC]
    datasource_np: Optional[NP_SRC]
    location: Location
    levels: List[Level]

    def __init__(self,
                 station: str,
                 obstime: datetime,
                 reltime: Optional[time],
                 nlevels: int,
                 datasource_p: Optional[P_SRC],
                 datasource_np: Optional[NP_SRC],
                 location: Location,
                 origin: str = None):
        self.station = station
        self.obstime = obstime
        self.reltime = reltime
        self.nlevels = nlevels
        self.datasource_p = datasource_p
        self.datasource_np = datasource_np
        self.location = location
        self.levels = []

    @property
    def __geo_interface__(self):
        return self.location.__geo_interface__

    def add(self, level: Level):
        if len(self.levels) < self.nlevels:
            self.levels.append(level)

    def header(self) -> str:
        return f"{self.station}\t{self.obstime.isoformat()}\t{self.nlevels:>4} levels"

    def to_json(self) -> str:
        import json

        class _SoundingEncoder(json.JSONEncoder):
            def default(self, x):
                if isinstance(x, (Sounding.Level, Location)):
                    return x.__dict__
                elif isinstance(x, (datetime, time, timedelta)):
                    return str(x)
                elif isinstance(x, (P_SRC, NP_SRC, LevelType.Major, LevelType.Minor, QualityFlag)):
                    return str(x.name).lower()
                else:
                    return super().default(x)
        return json.dumps(self.__dict__, cls=_SoundingEncoder, indent=4)
