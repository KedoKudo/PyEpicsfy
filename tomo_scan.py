#!/usr/bin/env python

"""
Perform a tomography scan with given configuration file(yaml).

Usage:
    tomo_6bm.py  [-dqh]  <CONFIGFILE>
 
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

@dataclass
class TomoScan:
    """
    scan plan for tomogarphy scan
    """
    config_file: str
    verbose: bool = True
    dry_run: bool = False

    def __post_init__(self):
        # parse the scan configuration file
        if self.verbose:
            print(f"-- parsing scan config file: {self.config_file}")
        
        with open(self.config_file) as f:
            self._config = yaml.safe_load(f)
        
        print(self._config)

    @log_event
    def start(self, monitor=False):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def reset(self):
        pass

    def stop(self, cache_position=True):
        # tomoscan_cleanup
        pass

    # def _check_beam(self):
    #     # check if beam is present
    #     _pv = f"{self._config['shutter']['PV']}:STA_A_FES_OPEN_PL"
    #     _logged = False
    #     while(epics.caget(_pv) == "OFF"):
    #         if not _logged:
    #             self._log(f"@{datetime.now()}, shutter is closed, waiting...")
    #             _logged = True
    #         time.sleep(60)
    #     # log beam back on
    #     self._log(f"@{datetime.now()}, shutter is reopened, continue scan...")


# ----- Start -----
if __name__ == "__main__":
    args = docopt(__doc__, version=0.1)
    in_dryrun = bool(args['--dry-run'])
    in_verbose = bool(not(args['--quiet']))
    
    freescan_6bm = TomoScan(args['<CONFIGFILE>'], 
                            verbose=in_verbose,
                            dry_run=in_dryrun,
                            )

