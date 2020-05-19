#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pigra",
    version="1.0.1",
    description="A Python IGRA v2 parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pixel-ports/pigra",
    author="Fabien Battello",
    author_email="fabien.battello@orange.com",
    license="Apache 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8"
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.8"
)
