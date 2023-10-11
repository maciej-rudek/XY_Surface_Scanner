
from ctypes import *
import time

from src.scan_data import ImCont, SemiMode, DwfData, ScanParam, Status, PictureData, SemiMode
from src.device_conf.device import *
from src.device_conf.device_semi import Device_semi
from src.files_operation import FileOperations


class Mode_semi:
    
    stan = 0
    WAIT_START = 0.2   
    
    def Scan():
        resolution = ScanParam.resolution
        buff_size = SemiMode.buf_size
        
        if (ScanParam.scan == Status.START):
            
            cvalid = Device_semi.Get_conti_data()
            
            if(cvalid.value == SemiMode.buf_size):
                Device_semi.Upadate_sample_oCH()
                Device_semi.Set_shift_aqusition()
                time.sleep(0.02)
                Device_semi.Set_semi_sin_output()
                # Device_semi.Start_on_once()
                PictureData.CHA[ImCont.x, 0:buff_size] = SemiMode.f_ch1
                PictureData.CHB[ImCont.x, 0:buff_size] = SemiMode.f_ch2
                ImCont.x = ImCont.x + 1
            
            if(ImCont.y >= resolution):
                ScanParam.scan = Status.STOP
                ImCont.x = 0
                ImCont.y = 0
                FileOperations.save_manager_files()
        else:
            Device_semi.Get_conti_data()
                
        for i in range(SemiMode.buf_size):
            SemiMode.f_ch1[i] = float(SemiMode.DataCH1[i])
            SemiMode.f_ch2[i] = float(SemiMode.DataCH2[i])
        
        time.sleep(Mode_semi.WAIT_START)