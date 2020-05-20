#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pigra.parser import IgraParser


def main():

    # parse sounding data
    parser = IgraParser.from_file("ASM00094703-data.txt.zip")

    # outputs general info about parsed data : stations, observations number and date range
    parser.analyze()


if __name__ == '__main__':
    main()
