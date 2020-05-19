#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pigra.parser import IgraParser
from pigra.utils import stream_from


def main():

    # input data from the sample file
    stream = stream_from("ASM00094703-data.txt.zip")

    # parse sounding data
    parser = IgraParser(stream)

    # outputs headers of the 5 first soundings
    parser.head()


if __name__ == '__main__':
    main()
