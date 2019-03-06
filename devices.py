#!/usr/bin/env python

import epics
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


if __name__ == "__main__":
    pass