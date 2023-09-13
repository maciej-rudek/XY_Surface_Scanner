
from ctypes import *
import time

from src.scan_data import ImCont, ContinuousMode, DwfData, ScanParam, Status, PictureSCS
from src.device_conf.device import *
from src.device_conf.device_conti import Device_conti


class Mode_continuous:
    
    time_to_watch = 0.0
    
    def Scan():
        WAIT_START = 0.2
        Wait_stop = ( 1 / ContinuousMode.hzAcq[0].value ) * 2
        resolution = ScanParam.resolution
        hzAcq_B = Wait_stop *  resolution 
        
        Device_conti.Get_conti_data()
        
        for i in range(ContinuousMode.buf_size):
            ContinuousMode.f_ch1[i] = float(ContinuousMode.DataCH1[i])
            ContinuousMode.f_ch2[i] = float(ContinuousMode.DataCH2[i])
        
        if (ScanParam.scan == Status.START):
            time.sleep(Wait_stop)
            Mode_continuous.time_to_watch = Mode_continuous.time_to_watch + Wait_stop
            watch = Mode_continuous.time_to_watch
            if (hzAcq_B <= watch):
                ScanParam.scan = Status.STOP
                Mode_continuous.time_to_watch = 0
        else:
            Mode_continuous.time_to_watch = 0
            time.sleep(WAIT_START)
    