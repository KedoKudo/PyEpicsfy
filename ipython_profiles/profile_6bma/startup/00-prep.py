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
RE.md['beamline_id'] = 'APS 6-BM-B'
RE.md['proposal_id'] = 'internal test'
RE.md['pid'] = os.getpid()
RE.md['login_id'] = USERNAME + '@' + HOSTNAME
RE.md['BLUESKY_VERSION'] = bluesky.__version__
RE.md['OPHYD_VERSION'] = ophyd.__version__
RE.md['apstools_VERSION'] = apstools.__version__
RE.md['SESSION_STARTED'] = datetime.isoformat(datetime.now(), " ")

