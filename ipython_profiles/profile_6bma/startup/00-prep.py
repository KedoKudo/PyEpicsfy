# Setup script for using BlueSky at 6-BM-A
print(f'Initializing IPython environment using {__file__}')

# -----
print('Config the meta-data handler...\n')
from databroker import Broker
db = Broker.named("mongodb_config")

# -----
print('Create RunEngine RE')
import bluesky
from bluesky import RunEngine
from bluesky.callbacks.best_effort import BestEffortCallback
print('*** subscribe both mongodb and callback to RE')
RE = RunEngine({})
RE.subscribe(db.insert)
RE.subscribe(BestEffortCallback())

print('*** add beamline specific meta-data')
import os
from datetime import datetime
import apstools
import ophyd
import socket
import getpass
HOSTNAME = socket.gethostname() or 'localhost'
USERNAME = getpass.getuser() or '6-BM-A user'
RE.md['beamline_id'] = 'APS 6-BM-A'
RE.md['proposal_id'] = 'internal test'
RE.md['pid'] = os.getpid()
RE.md['login_id'] = USERNAME + '@' + HOSTNAME
RE.md['BLUESKY_VERSION'] = bluesky.__version__
RE.md['OPHYD_VERSION'] = ophyd.__version__
RE.md['apstools_VERSION'] = apstools.__version__
RE.md['SESSION_STARTED'] = datetime.isoformat(datetime.now(), " ")

print("*** checking beam status")
import apstools.devices as APS_devices
aps = APS_devices.ApsMachineParametersDevice(name="APS")

from ophyd import EpicsSignalRO
instrument_in_use = lambda : EpicsSignalRO("6bm:instrument_in_use", 
                                           name="instrument_in_use",
                                ).get()
try:
    RE.md['INSTRUMENT_IN_USE'] = instrument_in_use()
except TimeoutError as e:
    print(f"---receving error: {e}---")
    print("---switching to offline test mode---")
    offline_testmode = True
    RE.md['INSTRUMENT_IN_USE'] = False
finally:
    from pprint import pprint
    print("Current registered metadata:")
    pprint(RE.md)
    print("Update entries in RE.md if necessary")

import apstools.synApps_ophyd
calcs = apstools.synApps_ophyd.userCalcsDevice("6bma1:", name="calcs", )
hutch_light_on = lambda : bool(calcs.calc1.val.get())

# conducting experiment mode
in_production = aps.inUserOperations \
            and (instrument_in_use.get() in (1, "6-BM-A")) \
            and (not hutch_light_on)

# testing mode, supercede in_production
in_dryrun = True
