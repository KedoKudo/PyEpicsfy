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


if __name__ == "__main__":
    pass