The Python IGRAv2 parsing library
=================================

**pigra** 
- parses IGRA data according to the [IGRAv2 specifications](ftp://ftp.ncdc.noaa.gov/pub/data/igra/data/igra2-data-format.txt)
- defines a clean Sounding data-structure easy to work with
- processes records on the fly without storing the whole archive in memory
- allows to filter soundings by providing your own function (including geoboxing)
- handles output to json format or human-readable headers
- computes statistics
- unit-tested

License
--------

    Copyright (C) 2019 Orange

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.