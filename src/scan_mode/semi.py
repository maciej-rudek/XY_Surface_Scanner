
from ctypes import *
import time

from src.scan_data import ImCont, SemiMode, DwfData, ScanParam, Status, PictureSCS
from src.device_conf.device import *
from src.device_conf.device_semi import Device_semi


class Mode_semi:
    
    stan = 0
    
    def Scan():
        resolution = ScanParam.resolution
        
        WAIT_START = 0.2
        
        # if (ScanParam.scan == Status.START):
            # time.sleep(1)
                    
        Device_semi.Get_conti_data()
        
        for i in range(SemiMode.buf_size):
            SemiMode.f_ch1[i] = float(SemiMode.DataCH1[i])
            SemiMode.f_ch2[i] = float(SemiMode.DataCH2[i])
        
        if (ScanParam.scan == Status.START):
            if (Mode_semi.stan == 0):
                if (ImCont.x == (resolution)):
                    Mode_semi.stan = 1
                else:
                    ImCont.dir = 0
                    # PictureData.CH1[ImCont.y, ImCont.x] = np.mean(SampleMode.f_ch1[int(marg):int(maks-marg)])
                    # PictureData.CH2[ImCont.y, ImCont.x] = np.mean(SampleMode.f_ch2[int(marg):int(maks-marg)]) 
                ImCont.x = ImCont.x + 1
        
        time.sleep(WAIT_START)