#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pigra.parser import IgraParser


def main():

    # parse sounding data
    parser = IgraParser.from_file("ASM00094703-data.txt.zip")

    # outputs headers of the 5 first soundings
    parser.head()


if __name__ == '__main__':
    main()
