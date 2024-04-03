
from ctypes import *
import time
import numpy as np

from src.scan_data import ImCont, ContinuousMode, DwfData, ScanParam, Status, PictureData
from src.device_conf.device import *
from src.device_conf.device_conti import Device_conti
from src.files_operation.operation import File_Operation
from src.scan_mode.special import Once

class Mode_continuous:
    
    WAIT_START = 0.2
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
            
            if (actual == ContinuousMode.buf_size):
                ending = ContinuousMode.buf_size
                off = 4000
                point = ending - off
                for i in  range(point, ending - double_res, 1):
                    ofA = i
                    ofsetC = i + double_res
                    if ( (ContinuousMode.v_ch1[0:double_res] == ContinuousMode.f_ch1[ofA : ofsetC])).all():
                        line = int ((ending - i) / double_res) - 1
                        
                        for y_line in range(line):
                                y_lin = int(y_line + Mode_continuous.old_line)
                                if(y_lin < resolution):
                                    ofA = y_line * double_res + ofsetC
                                    ofB = (y_line * double_res) + resolution + ofsetC
                                    ofC = (y_line + 1) * double_res + ofsetC
                                    PictureData.CH1[y_lin, 0:resolution] = ContinuousMode.f_ch1[ofA : ofB]
                                    PictureData.CH2[y_lin, 0:resolution] = ContinuousMode.f_ch2[ofA : ofB]
                                    PictureData.CH3[y_lin, 0:resolution] = ContinuousMode.f_ch1[ofB : ofC]
                                    PictureData.CH4[y_lin, 0:resolution] = ContinuousMode.f_ch2[ofB : ofC]
                                    ContinuousMode.v_ch1[0:double_res] = ContinuousMode.f_ch1[ofA : ofC]
                                    ContinuousMode.v_ch2[0:double_res] = ContinuousMode.f_ch2[ofA : ofC]
                                else:
                                    break
                                
                        Mode_continuous.old_line = Mode_continuous.old_line + line
                                
            else:
                line = (actual - (actual % double_res)) / double_res
            
                if (line > 0 and line < resolution):
                        
                    for y_line in range(int(Mode_continuous.old_line), int(line), 1):
                        y_lin = y_line
                        if(y_lin < resolution):
                            ofA = y_line * double_res
                            ofB = (y_line * double_res) + resolution
                            ofC = (y_line + 1) * double_res
                            PictureData.CH1[y_lin, 0:resolution] = ContinuousMode.f_ch1[ofA : ofB]
                            PictureData.CH2[y_lin, 0:resolution] = ContinuousMode.f_ch2[ofA : ofB]
                            PictureData.CH3[y_lin, 0:resolution] = ContinuousMode.f_ch1[ofB : ofC]
                            PictureData.CH4[y_lin, 0:resolution] = ContinuousMode.f_ch2[ofB : ofC]
                            ContinuousMode.v_ch1[0:double_res] = ContinuousMode.f_ch1[ofA : ofC]
                            ContinuousMode.v_ch2[0:double_res] = ContinuousMode.f_ch2[ofA : ofC]
                        else:
                            break
            
                Mode_continuous.old_line = line
                
            if(Mode_continuous.old_line + line >= resolution):
                ScanParam.scan = Status.STOP
                File_Operation.save_manager_files()
                
            time.sleep(Wait_stop)
            

        else: # STOP SCAN
            Mode_continuous.max_y_lines = int(ContinuousMode.buf_size/double_res)
            
            ContinuousMode.v_ch1[0:double_res] = ContinuousMode.f_ch1[0 : double_res]
            ContinuousMode.v_ch2[0:double_res] = ContinuousMode.f_ch2[0 : double_res]
            
            PictureData.CH1 = np.zeros((resolution, resolution))
            PictureData.CH2 = np.zeros((resolution, resolution))
            PictureData.CH3 = np.zeros((resolution, resolution))
            PictureData.CH4 = np.zeros((resolution, resolution))
            
            # PictureData.reshape_CH1234(Mode_continuous.max_y_lines, resolution)
            PictureData.reshape_CH1234(resolution, resolution)
            Mode_continuous.old_line = 0
            time.sleep(Mode_continuous.WAIT_START)
            actual = 0