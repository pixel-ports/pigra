#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="pigra",
    version="0.9.2",
    description="Python IGRA parser",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitpixel.satrdlab.upv.es/orange",
    author="Fabien Battello",
    author_email="fabien.battello@orange.com",
    license="Apache 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache 2.0 License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["pigra"],
    include_package_data=True,
    install_requires=[]
)
