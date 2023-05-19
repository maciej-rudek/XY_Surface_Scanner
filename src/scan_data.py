from dataclasses import dataclass
import numpy as np
from ctypes import *
from enum import Enum

MAX_VOLTAGE = 5.0
MAX_AREA = 100

class Status(Enum):
    START = "start"
    STOP = "stop"
    EXIT = "exit"

@dataclass
class logtime_s:
    start = ""
    end = ""
    duration = ""
    
@dataclass
class DwfData:
    hzAcq = [c_double(450000), c_double(450000)]
    cAvailable = c_int()
    cLost = c_int()
    cCorrupted = c_int()
    fLost = 0
    fCorrupted = 0
    version = ""
    status = ""
    logError = ""
    logTime = logtime_s


@dataclass
class ImCont:
    """Picture params"""
    dir = 0
    x = 0
    y = 0
    oY = 0
    
@dataclass
class PictureSCS:
    """Picture Scan Control Status"""
    direction = 0
    x_pos = 0
    y_pos = 0
    line = 0

@dataclass
class ScanParam:
    scan = Status.STOP
    resolution = 20
    area = 100
    oxy = MAX_VOLTAGE * area / MAX_AREA
    offset_x = 0
    offset_y = 0

@dataclass
class ScanSample:
    sample = 10000
    DataCH1: c_double = (c_double*sample)()
    DataCH2: c_double = (c_double*sample)()
    f_ch1 = np.arange(sample, dtype=float)
    f_ch2 = np.arange(sample, dtype=float)
    

@dataclass
class PictureData:
    CH1: float = np.zeros((ScanParam.resolution, ScanParam.resolution))
    CH2: float = np.zeros((ScanParam.resolution, ScanParam.resolution))
    CH3: float = np.zeros((ScanParam.resolution, ScanParam.resolution))
    CH4: float = np.zeros((ScanParam.resolution, ScanParam.resolution))
    line: int = 0


def print_class(what_class):
    my_class = what_class.__dict__
    # print(my_class)
    for name, value in my_class.items():
        if not name.startswith('__'):
            print('  ', name, ' = ', value)