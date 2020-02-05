#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from shapely.geometry import shape, box, Polygon

from pigra.parser import IgraParser

def main():
    poly: Polygon = box(22.0, 40.0, 23.0, 41.0) # approx geobox around Thessaloniki

    parser = IgraParser(f_match=lambda x: shape(x.position).within(poly))

    for sounding in parser.parse():
        print(sounding)


if __name__ == '__main__':
    main()