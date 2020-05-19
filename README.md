# pigra

[![PyPI Latest Release](https://img.shields.io/pigra/v/pigra)](https://pypi.org/project/pigra/)
[![License badge](https://img.shields.io/github/license/pixel-ports/pigra)](https://opensource.org/licenses/Apache-2.0)
[![Python version](https://img.shields.io/pypi/pyversions/pigra)](https://pypi.org/project/pigra/)

## What is it ?

A Python parsing library for the IGRA v2 format.

## Key Features

- parses IGRA data according to the [IGRAv2 specifications](ftp://ftp.ncdc.noaa.gov/pub/data/igra/data/igra2-data-format.txt)
- defines a clean Sounding data-structure easy to work with
- processes records on the fly without storing the whole archive in memory
- allows to filter soundings by providing your own function (including geoboxing)
- outputs to JSON format and human-readable headers
- computes statistics
- no dependencies
- unit-tested

## Where to get it
The source code is currently hosted on GitHub at :
https://github.com/pixel-ports/pigra

Binary installer for the latest released version is available at the [Python
package index](https://pypi.org/project/pigra).

```sh
pip install pigra
```

## License
[Apache 2.0](LICENSE)

## Documentation
Have a look at the `examples` directory.

## Background
Work on ``pigra`` started at [Orange](https://www.orange.com) in 2019 for the needs of the [PIXEL](https://pixel-ports.eu) european project.

## Funding

``pigra`` has been developed as part of the [PIXEL](https://pixel-ports.eu) project, H2020, funded by the EC under Grant Agreement number [769355](https://cordis.europa.eu/project/id/769355).