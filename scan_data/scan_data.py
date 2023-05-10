from dataclasses import dataclass
import numpy as np
from ctypes import *


@dataclass
class DwfData:
    hzAcq = [c_double(450000), c_double(450000)]
    cAvailable = c_int()
    cLost = c_int()
    cCorrupted = c_int()
    fLost = 0
    fCorrupted = 0
    version = ""
    logError = ""


@dataclass
class ImCont:
    resolution = 200
    dir = 0
    x = 0
    y = 0
    oY = 0
    sample = 10000
    

@dataclass
class ImCH:
    CH1: float = np.zeros((ImCont.resolution, ImCont.resolution))
    CH2: float = np.zeros((ImCont.resolution, ImCont.resolution))
    CH3: float = np.zeros((ImCont.resolution, ImCont.resolution))
    CH4: float = np.zeros((ImCont.resolution, ImCont.resolution))
    line: int = 0


@dataclass
class ScanData:
    DataCH1: c_double = (c_double*ImCont.sample)()
    DataCH2: c_double = (c_double*ImCont.sample)()
    f_ch1 = np.arange(ImCont.sample, dtype=float)
    f_ch2 = np.arange(ImCont.sample, dtype=float)