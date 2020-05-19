#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pigra.parser import IgraParser
from pigra.utils import stream_from


def main():

    # input data from the sample file
    stream = stream_from("ASM00094703-data.txt.zip")

    # parse sounding data
    parser = IgraParser(stream)

    # for each sounding display a human-readable header followed by the full JSON format
    for sounding in parser.parse():
        print(sounding.header())
        print(sounding.to_json())


if __name__ == '__main__':
    main()
