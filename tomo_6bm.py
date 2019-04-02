#!/usr/bin/env python

"""
Perform a tomography scan with given configuration file(yaml).

Usage:
    tomo_6bm.py  [-dqh]  <DEVICES> <SCAN>
 
Options:
-d, --dry-run           Test mode (no execuation)
-q, --quiet             Run/Test in quiet mode
-h, --help              Show this message
--version               Show version

"""

import epics
import yaml
import time
import warnings
import numpy as np
from dataclasses import dataclass
from datetime  import datetime
from docopt import docopt
from tqdm   import tqdm
from pymongo import MongoClient

from devices import Shutter
from devices import AreaDetector
from utility import log_event
from utility import load_config


def init_devices(conf_devices):
    """Initialize all devices described in the config"""
    devices = {}
    # -- init shutter
    devices['shutter'] = Shutter.from_config(conf_devices['shutter'])
    # -- init area detector
    # NOTE:
    #   no call is made to the hardwire until init() is called
    devices['detector'] = AreaDetector.from_config(conf_devices['areaDetector'])
    # -- init motors

    return devices


def init_scan(conf_scans):
    """Preparation work for scan"""
    scans = {}
    
    return scans


# ----- Start -----
if __name__ == "__main__":
    # CLI parsing
    args = docopt(__doc__, version=0.1)
    in_dryrun = bool(args['--dry-run'])
    in_verbose = bool(not(args['--quiet']))

    # Initialize all devices with given configurations
    devices = init_devices(load_config(args['<DEVICES>']))
    scans = init_scan(load_config(args['<SCAN>']))

    # Collect flat/white field images
    

    # Collect projections (step motion)

    # Collect flat/white field imasge

    # Collect dark field images