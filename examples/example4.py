#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Same as example3.py but incoming data from stdin

from pigra.parser import IgraParser


def main():

    # parse sounding data from standard input
    # example : cat ASM00094703-data.txt | python example4.py
    parser = IgraParser()

    # for each sounding display a human-readable header followed by the full JSON format
    for sounding in parser.parse():
        print(sounding.header())
        print(sounding.to_json())


if __name__ == '__main__':
    main()
