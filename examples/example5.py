#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Running this example requires shapely
# pip install shapely

from shapely.geometry import shape, box, Polygon

from pigra.parser import IgraParser


def main():
    # approx geobox around Thessaloniki
    poly: Polygon = box(22.0, 40.0, 23.0, 41.0)

    # parses soundings from standard input
    # outputs only soundings in the given area
    parser = IgraParser(f_match=lambda x: shape(x.location).within(poly))

    for sounding in parser.parse():
        print(sounding)


if __name__ == '__main__':
    main()
