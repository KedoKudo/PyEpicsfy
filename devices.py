#!/usr/bin/env python

import epics
import numpy as np
from dataclasses import dataclass


@dataclass
class Shutter:
    devicePV: str
    status: str
    on: str
    off: str

    @property
    def is_open(self):
        return not self.is_closed

    @property
    def is_closed(self):
        return(self.check_status() == "OFF")

    def check_status(self):
        return epics.caget(f"{self.devicePV}:{self.status}")

    def open(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    @staticmethod
    def from_config(config_dict):
        return Shutter(config_dict['devicePV'],
                       config_dict['status'],
                       config_dict['on'],
                       config_dict['off'],
                      )


@dataclass
class Camera:
    parentPV: str
    devicePV: str
    numImgs: int
    imageMode: str
    triggerMode: str
    acquireTime: float
    gain: float
    timeout: float

    def __post_init__(self):
        self.acquirePeriod = self.acquireTime + 0.01
        self.__pv = f"{self.parentPV}:{self.devicePV}"
    
    @property
    def pvlist(self):
        return [f"{self.__pv}:{me}" 
                    for me in ["NumImages", "ImageMode", "TriggerMode",
                               "AcquireTime", "AcquirePeriod", "Gain",
                    ]
                ]
    
    @property
    def pvvals(self):
        return [self.numImgs, self.imageMode, self.triggerMode, 
                self.acquireTime, self.acquirePeriod, self.gain,
            ]
    
    @property
    def pvs(self):
        return dict(zip(self.pvlist, self.pvvals))

    # poor man's way to deal with the inconsistent naming among
    # different epics instruments/devices
    @property
    def nframes(self):
        return epics.caget(f"{self.__pv}:NumImages.VAL")

    @nframes.setter
    def nframes(self, val):
        epics.caput(f"{self.__pv}:NumImages", val, 
                    wait=True, timeout=self.timeout)
    
    def init(self):
        epics.caput_many(self.pvlist, 
                         self.pvvals, 
                         wait='all', put_timeout=self.timeout,
                         )
    
    @staticmethod
    def from_config(parentPV, config_dict):
        return Camera(
            parentPV,
            config_dict['devicePV'],
            config_dict['NumImages'],
            config_dict['ImageMode'],
            config_dict['TriggerMode'],
            config_dict['AcquireTime'],
            config_dict['gain'],
            config_dict['timeout'],
            )


@dataclass
class Plugin:
    parentPV: str
    devicePV: str
    timeout: float
    pvs: dict

    # note:
    # Provided no modifications are made to the dictionary, 
    # the order is maintained among iterations
    def __post_init__(self):
        self.__pv = f"{self.parentPV}:{self.devicePV}"
        for key, val in self.pvs.items():
            setattr(self, key, val)

    @property
    def pvlist(self):
        return [f"{self.__pv}:{me}" for me, _ in self.pvs.items()]

    @property
    def pvvals(self):
        return [me for _, me in self.pvs.items()]
    
    def init(self):
        epics.caput_many(self.pvlist,
                         self.pvvals,
                         wait='all', put_timeout=self.timeout,
                         )

    @property
    def nframes(self):
        """read nframes from device"""
        # not an elegent way to handle the inconsistent naming,
        # but it should work
        if self.pvs.has_key("NumFilter"):
            _pv = f"{self.__pv}:NumFilter"
        elif self.pvs.has_key("NumCapture"):
            _pv = f"{self.__pv}:NumCapture"
        else:
            raise AttributeError("Cannot find nframes entry")
        
        return epics.caget(f"{_pv}.VAL")
    
    @nframes.setter
    def nframes(self, val):
        """set nframes to plugin"""
        if self.pvs.has_key("NumFilter"):
            _pv = f"{self.__pv}:NumFilter"
        elif self.pvs.has_key("NumCapture"):
            _pv = f"{self.__pv}:NumCapture"
        else:
            raise AttributeError("Cannot find nframes entry")
        # now send the value to epics
        epics.caput(_pv, val,
                    wait=True, timeout=self.timeout
                   )

    @staticmethod
    def from_config(parentpV, config_dict):
        return Plugin(parentpV,
                      config_dict['devicePV'],
                      config_dict['timeout'],
                      config_dict['pvs'],
        )


@dataclass
class AreaDetector:
    """
    This class was intended as an abstraction for all area detectors
    used at APS.  However, due to the inconsistent naming scheme
        ***
        for instance, the same concept "number of frames" are named as
        "NumImages" in the camera ca, "NumFilter" in the procesing plugins,
        and "NumCapture" in the file io plugin.
        ***
    it is difficult to make it work for all cases.  So a workaround
    would be use this one as a base class and reimplement the getter and
    setter.
    """
    devicePV: str
    config_dict: str

    def __post_init__(self):
        self.cameras = [Camera.from_config(self.devicePV,cfg)
                            for _, cfg in self.config_dict['cameras']
                       ]
        self.plugins = [Plugin.from_config(self.devicePV,cfg)
                            for _, cfg in self.config_dict['plugins']
                       ]
    
    def init(self):
        """ Initialize all cameras and plugins."""
        for cam in self.cameras:
            cam.init()
        for plg in self.plugins:
            plg.init()

    @property
    def nframes(self):
        _nframes = [cam.nframes for cam in self.cameras]
        _nframes += [plugin.nframes for plugin in self.plugins]
        
        if AreaDetector._is_uniform(_nframes):
            return np.average(_nframes).astyep(np.int)
        else:
            raise ValueError("Inconsistent nframes in detector settings")

    @nframes.setter
    def nframes(self, val):
        """set nframes to all cameras and plugins"""
        for cam in self.cameras:
            cam.nframes = val
        for plugin in self.plugins:
            plugin.nframes = val

    @staticmethod
    def _is_uniform(ndarray, tol=1e-4):
        ndarray = np.array(ndarray)
        delta = np.absolute(np.average(ndarray - ndarray.mean))
        return delta < tol


@dataclass
class Motor:
    devicePV: str


if __name__ == "__main__":
    pass