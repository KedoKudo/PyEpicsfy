# prefined plans for tomo scan at 6bma
_sep = u"🙊"*30
print(f'{_sep}\nCaching pre-defined scan plans with {__file__}')

import numpy                 as np
import bluesky.plans         as bp
import bluesky.preprocessors as bpp
import bluesky.plan_stubs    as bps


# ----
# Dark/White flat field
# NOTE:
#    det is a global var that refers to the detector
def collect_background(n_images, 
                       n_frames,
                       output='tiff',
    ):
    """collect n_images backgrounds with n_frames per take"""
    yield from bps.mv(det.cam.acquire, 0)

    set_output_type(output)
    
    for k,v in {
        "reset_filter":     1,
        "num_filter":       n_frames,
    }.items(): det.proc1.stage_sigs[k] = v
        
    for k,v in {
        "trigger_mode": "Internal",
        "image_mode":   "Multiple",
        "num_images":   n_frames,
    }.items(): det.cam.stage_sigs[k] = v

    @bpp.stage_decorator([det])
    @bpp.run_decorator()
    def scan():
        yield from bps.trigger_and_read([det]) 
    
    return (yield from scan())


# ----
# Projections (step)
def step_scan(n_images, 
              n_frames,
              angs,           # list of angles where images are taken
              output='tiff',
    ):
    """collect proejctions by stepping motors"""
    set_output_type(output)

    for k, v in {
        "enable":           1,         # toggle on proc1
        "reset_filter":     1,         # reset number_filtered
        "num_filter":       n_frames,
    }.items(): det.proc1.stage_sigs[k] = v
    
    for k, v in {
        "num_images":   n_frames,      
    }.items(): det.cam.stage_sigs[k] = v

    @bpp.stage_decorator([det])
    @bpp.run_decorator()
    def scan_closure():
        for ang in angs:
            yield from bps.checkpoint()
            yield from bps.mv(preci, ang)
            yield from bps.trigger_and_read([det])
    
    return (yield from scan_closure())


# ----
# Projections (fly)
def fly_scan():
    """collect projections using fly scan feature"""
    pass


# ----
# Example bundled tomo characterization scan
config_tomo_step = {
    "n_white"        :  10,
    "n_dark"         :  10,
    "samOutDist"     : -5.00,           # mm
    "omega_step"     :  0.25,           # degrees
    "acquire_time"   :  0.05,           # sec
    "acquire_period" :  0.05+0.01,      # sec
    "time_wait"      : (0.05+0.01)*2,   # sec
    "omega_start"    :  -180,           # degrees
    "omega_end"      :  180,            # degrees
    "n_frames"       :  5,              # proc.n_filters, cam.n_images
    "output"         : "tiff",          # output format ['tiff', 'hdf5']
}
def tomo_step(config_dict):
    """
    The master plan pass to RE for
    
    1. pre-white-field background collection
    2. projection collection
    3. post-white-field background collection
    4. post-dark-field background collection

    NOTE:
    see config_tomo_step for key inputs
    """
    pass



# ----
# Fly scan bundle example
config_tomo_step = {
    "n_white"        :  10,
    "n_dark"         :  10,
}
def tomo_fly(config_dict):
    """
    The master plan pass to RE for
    
    1. pre-white-field background collection
    2. projection collection
    3. post-white-field background collection
    4. post-dark-field background collection

    NOTE:
    see config_tomo_fly for key inputs
    """
    pass


print(f"Done with {__file__}\n{_sep}\n")
