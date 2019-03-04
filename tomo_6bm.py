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
import numpy as np
from dataclasses import dataclass
from docopt import docopt

@dataclass
class TomoScan:
    """
    scan plan for tomogarphy scan
    """
    mode: str
    config_file: str
    verbose: bool = True
    dry_run: bool = False

    def __post_init__(self):
        # parse the scan configuration file
        if self.verbose:
            print(f"--parsing scan config file: {self.config_file}")
        pass
    
    def start(self, monitor=False):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self, cache_position=True):
        pass


if __name__ == "__main__":
    args = docopt(__doc__, version=0.1)

    print(args)
    
    freescan_6bm = TomoScan('fly', 
                            'config.yml', 
                            verbose=bool(not(args['--quiet'])),
                            dry_run=bool(args['--dry-run']),
                            )

    print(freescan_6bm)