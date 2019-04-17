# define devices used for tomo scan at 6BM

# ----
# Shutter
from bluesky.suspenders import SuspendFloor
print("Setting up Shutter")
if in_production:
    # define the real shutter used at 6BMA@APS
    # NOTE: 
    #   this requires connection to the hardware, otherwise a connection error will be raised

    A_shutter = APS_devices.ApsPssShutterWithStatus(
            "6bmb1:rShtrA:",
            "PA:06BM:STA_A_FES_OPEN_PL",
            name="A_shutter",
        )
    A_shutter.pss_state
    # no scans until A_shutter is open
    suspend_A_shutter = SuspendFloor(A_shutter.pss_state, 1)
    # NOTE:
    # since tomo scan take dark field images with shutter colosed, the
    # suspender installation for A_shutter is located in the plan for
    # granular control.
    
    # no scans if aps.current is too low
    suspend_APS_current = SuspendFloor(aps.current, 2, resume_thresh=10)
    RE.install_suspender(suspend_APS_current)

else:
    # for testing during dark time (no beam, shutter closed by APS)
    A_shutter = APS_devices.SimulatedApsPssShutterWithStatus(name="A_shutter")
    suspend_A_shutter = SuspendFloor(A_shutter.pss_state, 1)
    print("---use simulated shutter---")

# ----
# Motors
from ophyd import MotorBundle
from ophyd import Component
from ophyd import EpicsMotor

class TomoStage(MotorBundle):
    #rotation
    preci = Component(EpicsMotor, "6bmpreci:m1", name='preci')    
    samX = Component(EpicsMotor, "6bma1:m19", name='samX')
    samY = Component(EpicsMotor, "6bma1:m18", name="samY")

print("Setting up motors")
if in_production or in_dryrun:
    tomostage = TomoStage(name='tomostage')

    samx  = tomostage.samX
    samy  = tomostage.samY
    preci = tomostage.preci

else:
    tomostage = MotorBundle()
    tomostage.preci = sim.motor
    tomostage.samX = sim.motor
    tomostage.samY = sim.motor
    print("using simulated detectors")


# ----
# Area Detector