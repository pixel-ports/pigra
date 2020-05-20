#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pigra.parser import IgraParser


def main():

    # parse sounding data
    parser = IgraParser.from_file("ASM00094703-data.txt.zip")

    # for each sounding display a human-readable header followed by the full JSON format
    for sounding in parser.parse():
        print(sounding.header())
        print(sounding.to_json())


if __name__ == '__main__':
    main()
