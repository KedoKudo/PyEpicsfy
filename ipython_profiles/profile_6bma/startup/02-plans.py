# prefined plans for tomo scan at 6bma
_sep = u"🙊"*30
print(f'{_sep}\nCaching pre-defined scan plans with {__file__}')

import bluesky.plans         as bp
import bluesky.preprocessors as bpp
import bluesky.plan_stubs    as bps


# ----
# Dark/White flat field
def collect_background(n_images, 
                       n_frames,
                       detector,
                       output='tiff',
    ):
    """collect n_images backgrounds with n_frames per take"""
    yield from bps.mv(detector.cam.acquire, 0)

    if output.lower() in ['tif', 'tiff']:
        for k,v in {
            "num_capture": n_images,
            "capture":     1,
        }.items(): detector.tiff1.stage_sigs[k] = v
    elif output.lower() in ['hdf', 'hdf1', 'hdf5']:
        for k,v in {
            "num_capture": n_images,
            "capture":     1,
        }.items(): detector.hdf1.stage_sigs[k] = v
    else:
        raise ValueError(f"Unknown output format {output}")
    
    for k,v in {
        "reset_filter":     1,
        "num_filter":       n_frames,
    }.items(): detector.proc1.stage_sigs[k] = v
        
    for k,v in {
        "trigger_mode": "Internal",
        "image_mode":   "Multiple",
        "num_images":   n_frames,
    }.items(): detector.cam.stage_sigs[k] = v

    @bpp.stage_decorator([detector])
    @bpp.run_decorator()
    def scan():
        yield from bps.trigger_and_read([detector]) 
    
    return (yield from scan())


# ----
# Projections (step)
def step_scan():
    """collect proejctions by stepping motors"""
    pass


# ----
# Projections (fly)
def fly_scan():
    """collect projections using fly scan feature"""
    pass


# ----
# Example bundled tomo characterization scan
def tomo_step():
    """
    The master plan pass to RE for
    
    1. pre-white-field background collection
    2. projection collection
    3. post-white-field background collection
    4. post-dark-field background collection
    """
    pass


print(f"Done with {__file__}\n{_sep}\n")
