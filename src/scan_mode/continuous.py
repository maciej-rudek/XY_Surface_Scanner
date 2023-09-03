
from ctypes import *
import time

from src.scan_data import ImCont, ContinuousMode, DwfData, ScanParam, Status, PictureSCS
from src.device_conf.device import *
from src.device_conf.device_conti import Device_conti


class Mode_continuous:
    
    def Colect_Data():
        Wait_time= ( 1/ContinuousMode.hzAcq[0].value ) * 2
        Device_conti.Get_conti_data()
        
        # procedure the collected data
        
        time.sleep(Wait_time)