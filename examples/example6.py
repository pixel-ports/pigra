#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Running this example requires shapely
# pip install shapely

from shapely.geometry import shape, box, Polygon

from pigra.parser import IgraParser


def main():
    # Australia bounding box
    australia: Polygon = box(
        113.338953078, -43.6345972634, 153.569469029, -10.6681857235)

    # filters soundings matching the given area
    parser = IgraParser.from_file(
        "ASM00094703-data.txt.zip", f_match=lambda x: shape(x.location).within(australia))

    for sounding in parser.parse():
        print(sounding.header())


if __name__ == '__main__':
    main()
