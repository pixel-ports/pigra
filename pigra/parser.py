#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from io import TextIOWrapper
from typing import Iterable, Generator, List, Optional, Callable
from copy import copy

from pigra.sounding import Sounding, Location
from pigra.constants import P_SRC, NP_SRC, LevelType, QualityFlag
from pigra.utils import stream_from


class SoundingException(Exception):
    pass


class IgraParser:

    @dataclass
    class Stats:
        lines: int = 0
        null: int = 0
        records: int = 0
        processed: int = 0
        filtered: int = 0
        errors: int = 0
        warnings: int = 0
        elapsed: timedelta = timedelta(seconds=0)

        def __eq__(self, other):
            if other.__class__ is not self.__class__:
                return NotImplemented
            # compare all attributes except elapsed
            s, o = copy(self.__dict__), copy(other.__dict__)
            s['elapsed'] = o['elapsed'] = None
            return s == o

    def __init__(self,
                 stream: Iterable = sys.stdin,
                 f_match: Callable[[Sounding], bool] = lambda x: True,
                 verbose=False):
        self.stream = stream
        self.filename = None
        self.f_match = f_match
        self.verbose = verbose
        self.stats = IgraParser.Stats()
        
    @classmethod
    def from_file(cls,
                  filename: str,
                  f_match: Callable[[Sounding], bool] = lambda x: True,
                  verbose=False):
         parser = cls(stream_from(filename), f_match, verbose)              
         parser.filename = filename
         return parser

    def parse(self) -> Generator:
        start = datetime.now()
        sounding: Optional[Sounding] = None
        for line in self.stream:
            self.stats.lines += 1
            if not line:
                self.stats.null += 1
                continue
            if line[0] == '#':
                if sounding:
                    yield sounding
                try:
                    sounding = self.parse_header(line)
                    self.stats.records += 1
                except Exception as e:
                    self.stats.errors += 1
                    if self.verbose:
                        print(f"ERROR : {e}\n{line=}", file=sys.stderr)
                    continue
                if self.f_match(sounding):
                    self.stats.processed += 1
                else:
                    self.stats.filtered += 1
                    sounding = None
            elif sounding:
                try:
                    level = self.parse_level(line)
                except Exception as e:
                    self.stats.warnings += 1
                    if self.verbose:
                        print(
                            f"WARNING : {e}\n{sounding.header()=}\n{line=}", file=sys.stderr)
                    continue
                sounding.add(level)
        if sounding:
            yield sounding
        self.stats.elapsed = datetime.now()-start

    def analyze(self):
        stations = set()
        start = datetime.max.replace(tzinfo=timezone.utc)
        end = datetime.min.replace(tzinfo=timezone.utc)
        for sounding in self.parse():  # consume all soundings
            stations.add(sounding.station)
            start = min(start, sounding.obstime)
            end = max(end, sounding.obstime)
        print(
            f"Found {len(stations)} station(s): {' '.join(x for x in stations)}.")
        print(
            f"Found {self.stats.records} observations ranging from {start} to {end}.")

    def head(self, n: int = 5):
        for sounding in (x for _, x in zip(range(n), self.parse())):
            print(sounding.header())

    def reset(self):
        if self.filename:
            self.stream = stream_from(self.filename)
            self.stats = IgraParser.Stats() 

    @staticmethod
    def parse_header(hdr: str) -> Sounding:
        if not hdr:
            raise SoundingException("Bad header string")
        if hdr[0] != '#':
            raise SoundingException("Missing # character")
        hdr = hdr.strip()
        if len(hdr) != 71:
            raise SoundingException("Bad header length")
        station = hdr[1:12]
        if hdr[24:26] == "99":  # missing hour
            fields = [int(x) for x in hdr[13:23].split()]
        else:
            fields = [int(x) for x in hdr[13:26].split()]
        obstime = datetime(*fields, tzinfo=timezone.utc)
        reltime = hdr[27:31]
        if reltime == "9999":  # missing release time
            reltime = None
        elif reltime[-2:] == "99":  # missing release time minute
            reltime = reltime[:2]
            reltime = datetime.strptime(reltime, "%H").time()
        else:
            reltime = datetime.strptime(reltime, "%H%M").time()
        nlevels = int(hdr[32:36])
        datasource_p, datasource_np = None, None
        if (datasource:=hdr[37:45].strip()) != "":
            datasource_p = P_SRC(datasource)
        if (datasource:=hdr[46:54].strip()) != "":
            datasource_np = NP_SRC(datasource)
        lat, lon = hdr[55:62], hdr[63:71]
        lat, lon = f"{lat[:-4]}.{lat[-4:]}", f"{lon[:-4]}.{lon[-4:]}"
        lat, lon = float(lat), float(lon)
        location = Location(lat, lon)
        return Sounding(station, obstime, reltime, nlevels, datasource_p, datasource_np, location)

    @staticmethod
    def parse_level(line: str) -> Sounding.Level:
        if not line:
            raise SoundingException("Bad level string")
        line = line.strip()
        if len(line) != 51:
            raise SoundingException("Bad level length")
        # major level type indicator
        major = LevelType.Major(int(line[0]))
        # minor level type indicator
        minor = LevelType.Minor(int(line[1]))
        # elapsed time
        if (value:=line[3:8]) in ("-8888", "-9999"):
            elapsed = None, QualityFlag(value)
        else:
            dt = datetime.strptime(value.strip(), "%M%S")
            elapsed = timedelta(minutes=dt.minute,
                                seconds=dt.second), QualityFlag.PASSED
        # pressure
        if (value:=line[9:15]) == "-9999":
            value = None
        else:
            value = int(value)
        if (flag:=line[15]) in (' ', 'A', 'B'):
            flag = QualityFlag(flag)
        else:
            flag = QualityFlag.ERROR
        pressure = value, flag
        # height
        if (value:=line[16:21]) in ("-8888", "-9999"):
            value = None
        else:
            value = int(value)
        if (flag:=line[21]) in (' ', 'A', 'B'):
            flag = QualityFlag(flag)
        else:
            flag = QualityFlag.ERROR
        height = value, flag
        # temperature
        if (value:=line[22:27]) in ("-8888", "-9999"):
            value = None
        else:
            value = int(value)/10
        if (flag:=line[27]) in (' ', 'A', 'B'):
            flag = QualityFlag(flag)
        else:
            flag = QualityFlag.ERROR
        temperature = value, flag
        # humidity
        if (value:=line[28:33]) in ("-8888", "-9999"):
            humidity = None, QualityFlag(value)
        else:
            humidity = int(value)/10, QualityFlag.PASSED
        # dew point
        if (value:=line[34:39]) in ("-8888", "-9999"):
            dewpoint = None, QualityFlag(value)
        else:
            dewpoint = int(value)/10, QualityFlag.PASSED
        # wind direction
        if (value:=line[40:45]) in ("-8888", "-9999"):
            winddir = None, QualityFlag(value)
        else:
            winddir = int(value), QualityFlag.PASSED
        # wind speed
        if (value:=line[46:51]) in ("-8888", "-9999"):
            windspeed = None, QualityFlag(value)
        else:
            windspeed = int(value)/10, QualityFlag.PASSED
        return Sounding.Level(major, minor, elapsed, pressure, height, temperature, humidity, dewpoint, winddir, windspeed)
