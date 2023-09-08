
from ctypes import *
import time

from src.scan_data import ImCont, ContinuousMode, DwfData, ScanParam, Status, PictureSCS
from src.device_conf.device import *
from src.device_conf.device_conti import Device_conti


class Mode_continuous:
    
    def Scan():
        Wait_time = ( 1 / ContinuousMode.hzAcq[0].value ) * 2
        
        Device_conti.Get_conti_data()
        
        for i in range(ContinuousMode.buf_size):
            ContinuousMode.f_ch1[i] = float(ContinuousMode.DataCH1[i])
            ContinuousMode.f_ch2[i] = float(ContinuousMode.DataCH2[i])
        
        time.sleep(Wait_time)
    