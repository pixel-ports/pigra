#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timezone
from pigra.parser import IgraParser


def main():

    start = datetime(1948, 3, 1, tzinfo=timezone.utc)
    end = datetime(1948, 4, 1, tzinfo=timezone.utc)
    
    # filters soundings observed on 1948, March
    parser = IgraParser.from_file(
        "ASM00094703-data.txt.zip", lambda x: start <= x.obstime <= end)

    for sounding in parser.parse():
        print(sounding.header())

if __name__ == '__main__':
    main()
