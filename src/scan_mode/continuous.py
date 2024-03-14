
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
    state = 0
    old_line = 0
    max_y_lines = 0
    tail = 0
    line_offset = 0

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
            
            line = (actual - (actual % double_res)) / double_res + Mode_continuous.line_offset
            
            if (line > 0 and line < resolution):
                
                for y_line in range(int(Mode_continuous.old_line), int(line), 1):
                    PictureData.CH1[y_line, 0:resolution] = ContinuousMode.f_ch1[(y_line * double_res) : ((y_line * double_res) + resolution)]
                    PictureData.CH2[y_line, 0:resolution] = ContinuousMode.f_ch2[(y_line * double_res) : ((y_line * double_res) + resolution)]
                    PictureData.CH3[y_line, 0:resolution] = ContinuousMode.f_ch1[((y_line * double_res) + resolution) : (y_line+1) * double_res]
                    PictureData.CH4[y_line, 0:resolution] = ContinuousMode.f_ch2[((y_line * double_res) + resolution) : (y_line+1) * double_res]
                    ContinuousMode.v_ch1[0:double_res] = ContinuousMode.f_ch1[y_line * double_res : (y_line+1) * double_res]
                    ContinuousMode.v_ch2[0:double_res] = ContinuousMode.f_ch2[y_line * double_res : (y_line+1) * double_res]
            
            Mode_continuous.old_line = line
            
            if (line == Mode_continuous.max_y_lines):
                
                tail = ContinuousMode.buf_size + Mode_continuous.tail - ( Mode_continuous.max_y_lines * double_res )   # reset of buffor to use
                Device_conti.Set_continuous_sin_output()
                time.sleep(Wait_stop) 
                actual = Device_conti.Get_conti_data() + tail #check if we can achive one full line
                
                for i in range(ContinuousMode.buf_size):
                    ContinuousMode.f_ch1[i] = float(ContinuousMode.DataCH1[i])
                    ContinuousMode.f_ch2[i] = float(ContinuousMode.DataCH2[i])
                    
                line = (actual - (actual % double_res)) / double_res
                Mode_continuous.line_offset = Mode_continuous.old_line + line
                Mode_continuous.old_line = 0
                print("line: ", line, ", line_offset: ", Mode_continuous.line_offset)
                # put data to picture - take line_offset insed of line 
            
                if (line > 0 and line < resolution):
                
                    for y_line in range(int(Mode_continuous.old_line), int(line), 1):
                        PictureData.CH1[y_line, 0:resolution] = ContinuousMode.f_ch1[(y_line * double_res) + tail : ((y_line * double_res) + resolution  + tail)]
                        PictureData.CH2[y_line, 0:resolution] = ContinuousMode.f_ch2[(y_line * double_res) + tail : ((y_line * double_res) + resolution  + tail)]
                        PictureData.CH3[y_line, 0:resolution] = ContinuousMode.f_ch1[((y_line * double_res) + tail + resolution) : (y_line+1) * double_res  + tail]
                        PictureData.CH4[y_line, 0:resolution] = ContinuousMode.f_ch2[((y_line * double_res) + tail + resolution) : (y_line+1) * double_res  + tail]
                        ContinuousMode.v_ch1[0:double_res] = ContinuousMode.f_ch1[y_line * double_res : (y_line+1) * double_res]
                        ContinuousMode.v_ch2[0:double_res] = ContinuousMode.f_ch2[y_line * double_res : (y_line+1) * double_res]
            
                Mode_continuous.tail = actual - (line * double_res)
            
            if(line == resolution):
                ScanParam.scan = Status.STOP
                File_Operation.save_manager_files()
                
            time.sleep(Wait_stop)
            

        else: # STOP SCAN
            Mode_continuous.max_y_lines = int(ContinuousMode.buf_size/double_res)
            Mode_continuous.tail = ContinuousMode.buf_size - Mode_continuous.max_y_lines
            
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