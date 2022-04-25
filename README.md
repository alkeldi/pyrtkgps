# pyrtkgps

`pyrtkgps` is a library for managing and configuring GPS and other GNSS chips. The main focus of this library is to provide support
for GPS modules with Real-Time Kinematic (RTK) positioning. Currently, GPS modules manufactured by `u-blox` are supported.

**Credit:** The base code for `pyrtkgps` was initially written for a Real-Time Kinematic GPS [experiment](https://github.com/janakj/gps-rtk)  at Columbia University.


## Current Status
<table>
  <tr>
    <th> Branch </th>
    <th> Build </th>
    <th> Package </th>
    <th> License </th>
  </tr>
  
  <tr>
    <td> master </td>
    <td>
      <a href="https://github.com/alkeldi/pyrtkgps/tree/master">
        <img src="https://github.com/alkeldi/pyrtkgps/actions/workflows/makefile.yml/badge.svg?branch=master" alt="Pylint: master"/>
      </a>
    </td>
    <td>
      <a href="https://pypi.org/project/pyrtkgps/">
        <img src="https://img.shields.io/pypi/v/pyrtkgps" alt="pypi: version"/>
      </a>    
    </td>
    <td rowspan="100%">
      <a href="https://github.com/alkeldi/pyrtkgps/blob/master/LICENSE">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"/>
      </a>
    </td>
  </tr>
  
  <tr>
    <td> test </td>
    <td>
      <a href="https://github.com/alkeldi/pyrtkgps/tree/test">
        <img src="https://github.com/alkeldi/pyrtkgps/actions/workflows/makefile.yml/badge.svg?branch=test" alt="Pylint: test"/>
      </a>
    </td>
    <td style='text-align: center;'>
      <a href="https://test.pypi.org/project/pyrtkgps/">
        <img src="https://img.shields.io/badge/pypi-(test)-red" alt="pypi: version"/>
      </a>  
    </td>
  </tr>
</table>


## Install
``` bash
pip install pyrtkgps
```

## Usage
The following is an example for configuring the `ZED-F9P` chip (from `u-blox`) as a base station.
The YAML file can be replaced with a YAML string if needed.
##### base_station.yml
``` yaml
RAM:
  UBX-CFG-VALSET:
    # enable survey-in mode
    - CFG-TMODE-MODE: 1
    - CFG-TMODE-SVIN_MIN_DUR: 60
    - CFG-TMODE-SVIN_ACC_LIMIT: 50000

    # disable NMEA on uart1
    - CFG-UART1OUTPROT-NMEA: 0

    # enable survey-in status output
    - CFG-MSGOUT-UBX_NAV_SVIN_UART1: 1

    # enable rtcm messages
    - CFG-MSGOUT-RTCM_3X_TYPE1005_UART1: 1
    - CFG-MSGOUT-RTCM_3X_TYPE1074_UART1: 1
    - CFG-MSGOUT-RTCM_3X_TYPE1084_UART1: 1
    - CFG-MSGOUT-RTCM_3X_TYPE1124_UART1: 1
    - CFG-MSGOUT-RTCM_3X_TYPE1230_UART1: 5
```

##### base_station.py
``` python
from serial import Serial
import pyrtkgps.ublox as ublox
from pyubx2.ubxreader import UBXReader

# connect to the uart1 port with baudrate 38400
uart1 = Serial("/dev/uart1", 38400)

# split the uart1 stream into a stream for each protocol (UBX, RTCM, NMEA)
virtual_streams = ublox.StreamMuxDemux(uart1)

# load the chip configuration from a YAML file (or use a YAML string)
config_file = open("./base_station.yml", "r")

# serialize the configuration file
sr = ublox.UBXSerializer
serialized_config = sr.serialize(config_file)

# close the configuration file
config_file.close()

# write serialized config to the ublox chip 
virtual_streams.UBX.write(serialized_config)

# print UBX output
ubr = UBXReader(virtual_streams.UBX)
while True:
    raw, msg = ubr.read()
    print(msg)
```
