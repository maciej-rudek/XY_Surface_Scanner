
from ctypes import *
import time

from src.scan_data import ImCont, ContinuousMode, DwfData, ScanParam, Status, PictureData
from src.device_conf.device import *
from src.device_conf.device_conti import Device_conti
from src.files_operation.operation import File_Operation


class Mode_continuous:
    
    WAIT_START = 0.2
    state = 0
    old_line = 0
    max_y_lines = 0

    def Scan():
        Wait_stop = ( 1 / ContinuousMode.hzAcq[0].value ) * 2
        resolution = ScanParam.resolution
        double_res = resolution * 2
        actual = Device_conti.Get_conti_data()
        
        for i in range(ContinuousMode.buf_size):
            ContinuousMode.f_ch1[i] = float(ContinuousMode.DataCH1[i])
            ContinuousMode.f_ch2[i] = float(ContinuousMode.DataCH2[i])
        
        if (ScanParam.scan == Status.START):
            
            Device_conti.First_configuration()
            
            line = (actual - (actual % double_res)) / double_res
            
            if((actual - 1) == ContinuousMode.buf_size):
                ScanParam.scan = Status.STOP
                ImCont.x = 0
                ImCont.y = 0
                # File_Operation.save_manager_files()
            
            if (line > 0 and line < Mode_continuous.max_y_lines):
                
                for y_line in range(int(Mode_continuous.old_line),int(line), 1):
                    PictureData.CHA[y_line, 0:double_res] = ContinuousMode.f_ch1[y_line * double_res : (y_line+1) * double_res]
                    PictureData.CHB[y_line, 0:double_res] = ContinuousMode.f_ch2[y_line * double_res : (y_line+1) * double_res]
            
            time.sleep(Wait_stop)
            Mode_continuous.old_line = line

        else:
            Mode_continuous.max_y_lines = int(ContinuousMode.buf_size/double_res)
            
            PictureData.reshape_CHAB(Mode_continuous.max_y_lines,double_res)
            Mode_continuous.old_line = 0
            time.sleep(Mode_continuous.WAIT_START)
            actual = 0