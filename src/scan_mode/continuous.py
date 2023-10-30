
from ctypes import *
import time

from src.scan_data import ImCont, ContinuousMode, DwfData, ScanParam, Status, PictureData
from src.device_conf.device import *
from src.device_conf.device_conti import Device_conti
from src.files_operation.operation import File_Operation


class Mode_continuous:
    
    WAIT_START = 0.2
    state = 0
    
    def Scan():
        Wait_stop = ( 1 / ContinuousMode.hzAcq[0].value ) * 2
        resolution = ScanParam.resolution
        old = 0
        space = 0
        
        actual = Device_conti.Get_conti_data()
        
        for i in range(ContinuousMode.buf_size):
            ContinuousMode.f_ch1[i] = float(ContinuousMode.DataCH1[i])
            ContinuousMode.f_ch2[i] = float(ContinuousMode.DataCH2[i])
        
        if (ScanParam.scan == Status.START):
            
            Device_conti.First_configuration()
            
            # PictureData.CHA[ImCont.x, 0:buff_size] = SemiMode.f_ch1
            # PictureData.CHB[ImCont.x, 0:buff_size] = SemiMode.f_ch2
            
            if(ContinuousMode.buf_size == actual):
                ScanParam.scan = Status.STOP
                ImCont.x = 0
                ImCont.y = 0
                # File_Operation.save_manager_files()
            
            if (Mode_continuous.state == 0):
                space = actual - old
                old = actual
            
            time.sleep(Wait_stop)

        else:
            time.sleep(Mode_continuous.WAIT_START)
            actual = 0