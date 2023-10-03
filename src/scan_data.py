from asyncio.windows_events import NULL
from ctypes.wintypes import DWORD
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
    SAVE = "save"
    YES = "yes"
    NO = "no"
    SAMPLE = "sample"
    SEMI = "semi"
    CONTINUOUS = "continuous"

@dataclass
class Logtime:
    start = ""
    end = ""
    duration = ""
    
@dataclass
class DwfData:
    # hzAcq = [c_double(450000), c_double(450000)]
    cAvailable = c_int()
    cLost = c_int()
    cCorrupted = c_int()
    fLost = 0
    fCorrupted = 0
    version = ""
    status = ""
    logError = ""
    logTime = Logtime
    logStat = Status.NO
    title = "SCAN"
    directory = "NoN"
    files = "000"
    clear_menu = False


@dataclass
class Dwf:
    dw = NULL
    hdwf = c_int()
    sts = c_byte()
    rghdwf = []

@dataclass
class ImCont:
    """Picture params"""
    dir = 0
    x = 0.0
    y = 0.0
    oY = 0
    
@dataclass
class PictureSCS:
    """Picture Scan Control Status"""
    direction = 0
    x_pos = 0
    y_pos = 0
    line = 0
    interpolate = Status.NO

@dataclass
class ScanParam:
    scan = Status.STOP
    scan_update = False
    mode = Status.SEMI
    mode_new = Status.SEMI
    resolution = 20
    area = 100
    oxy = MAX_VOLTAGE * area / MAX_AREA
    offset_x = 0
    offset_y = 0

@dataclass
class SampleMode: #ScanSample:
    sample = 10000
    hzAcq = [c_double(450000), c_double(450000)]
    DataCH1: c_double = (c_double*sample)()
    DataCH2: c_double = (c_double*sample)()
    f_ch1 = np.arange(sample, dtype=float)
    f_ch2 = np.arange(sample, dtype=float)
    
@dataclass
class ContinuousMode:
    sample = 10000
    hzAcq = [c_double(1), c_double(1)]
    buf_size = 1000
    phase_ch1 = c_double(90.0)
    phase_ch2 = c_double(90.0)
    DataCH1: c_double = (c_double*buf_size)()
    DataCH2: c_double = (c_double*buf_size)()
    f_ch1 = np.arange(buf_size, dtype=float)
    f_ch2 = np.arange(buf_size, dtype=float)


@dataclass
class SemiMode:
    sample = 10000
    hzAcq = [c_double(1), c_double(1)]
    buf_size = 250
    phase_ch1 = c_double(90.0)
    phase_ch2 = c_double(0.0)
    DataCH1: c_double = (c_double*buf_size)()
    DataCH2: c_double = (c_double*buf_size)()
    f_ch1 = np.arange(buf_size, dtype=float)
    f_ch2 = np.arange(buf_size, dtype=float)
    
@dataclass
class PictureData:
    CH1: float = np.zeros((ScanParam.resolution, ScanParam.resolution))
    CH2: float = np.zeros((ScanParam.resolution, ScanParam.resolution))
    CH3: float = np.zeros((ScanParam.resolution, ScanParam.resolution))
    CH4: float = np.zeros((ScanParam.resolution, ScanParam.resolution))
    line: int = 0
    save = Status.NO


def print_class(what_class):
    my_class = what_class.__dict__
    for name, value in my_class.items():
        if not name.startswith('__'):
            print('  ', name, ' = ', value)