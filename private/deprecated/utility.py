#!/usr/bin/env python

"""
Utility support for beamline control

Usage:
    utility test
    utility start

Options:
-h, --help          Show this message
--version           Show version
"""

import yaml
from functools import wraps
from datetime  import datetime
from docopt import docopt
from pymongo import MongoClient

def load_config(conf_f):
    """Read configuration to dict"""
    with open(conf_f, 'r') as f:
        conf_dict = yaml.safe_load(f)
    return conf_dict

def log_event(func, port=27017):
    def log_event_(*args, **kwds):
        client = MongoClient('localhost', port)
        db=client.test.events
        db.insert_one({
            "experiment": "test",
            "time": datetime.now(), 
            "func": func.__name__,
            "args": ",".join(map(str, args)),
            "keywords": ",".join(map(str, kwds)),
        })
        return func(*args, **kwds)
    return log_event_

@log_event
def testfunc(a, b):
    print(a+b)
    return a+b

if __name__ == "__main__":
    args = docopt(__doc__, version=0.1)

    if args['test']:
        testfunc(1,2)
    elif args['start']:
        print("run\n>> mongod  --dbpath ~/data/db\n")
    else:
        pass
