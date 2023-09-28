
from ctypes import *
import time

from src.scan_data import ImCont, SemiMode, DwfData, ScanParam, Status, PictureSCS, SemiMode
from src.device_conf.device import *
from src.device_conf.device_semi import Device_semi
from src.files_operation import FileOperations


class Mode_semi:
    
    stan = 0
    
    def Scan():
        resolution = ScanParam.resolution
        
        WAIT_START = 0.2   
        
        if (ScanParam.scan == Status.START):
            
            cvalid = Device_semi.Get_conti_data()
            
            if(cvalid.value == SemiMode.buf_size):
                Device_semi.Set_shift_aqusition()
                Device_semi.Upadate_sample_oCH()
                time.sleep(0.02)
                Device_semi.Set_semi_sin_output()
            
            if(ImCont.y > resolution):
                ScanParam.scan = Status.STOP
                ImCont.y = 0
                FileOperations.save_manager_files()
        else:
            
            Device_semi.Get_conti_data()
                
        for i in range(SemiMode.buf_size):
            SemiMode.f_ch1[i] = float(SemiMode.DataCH1[i])
            SemiMode.f_ch2[i] = float(SemiMode.DataCH2[i])
        
        time.sleep(WAIT_START)