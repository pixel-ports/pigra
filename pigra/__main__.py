#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from zipfile import ZipFile
from io import TextIOWrapper
from datetime import datetime, timezone
from typing import Iterable

from pigra.parser import IgraParser
from pigra.utils import stream_from, jsonfmt


def main():
    #stream = stream_from("/home/fieb7512/GRM00016622-data.txt.zip")
    start = datetime(2018, 1, 1, tzinfo=timezone.utc)
    end = datetime(2018, 1, 2, tzinfo=timezone.utc)
    parser = IgraParser.from_file("/home/fieb7512/GRM00016622-data.txt.zip", lambda x: start <= x.obstime <= end)
    jsonfmt("[") # open json array
    for sounding in parser.parse():
        jsonfmt(sounding.to_json(), indentlvl=1)
    jsonfmt("]") # close json array
    print(parser.stats, file=sys.stderr)


if __name__ == '__main__':
    main()
