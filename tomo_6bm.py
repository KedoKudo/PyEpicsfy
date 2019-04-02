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
from utility import log_event
from utility import load_config

def free_scan(scan_config):
    pass

# ----- Start -----
if __name__ == "__main__":
    args = docopt(__doc__, version=0.1)
    in_dryrun = bool(args['--dry-run'])
    in_verbose = bool(not(args['--quiet']))

    conf_devices = load_config(args['<DEVICES>'])
    conf_scan = load_config(args['<SCAN>'])

    print(conf_devices)
    print(conf_scan)

    # Initialize all devices with given configurations

    # Collect flat/white field images

    # Collect projections (step motion)

    # Collect flat/white field imasge

    # Collect dark field images