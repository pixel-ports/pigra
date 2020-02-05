#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pigra.parser import IgraParser
from pigra.utils import stream_from

def main():
    stream = stream_from("ASM00094703-data.txt.zip")
    parser = IgraParser(stream)
    # for sounding in parser.parse():
    #     print(sounding)
    #parser.analyze()
    parser.head()

if __name__ == '__main__':
    main()
