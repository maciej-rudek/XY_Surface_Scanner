import sys
import time

from src.device_conf.dwfconstants import *
from src.scan_data import Dwf, ImCont, SampleMode, SemiMode, DwfData, ScanParam, Status
from src.scan_mode.special import Once

class Device_semi:
    
    @Once.Run_once
    def First_configuration():
        Device_semi.Set_shift_aqusition()
        Device_semi.Set_semi_sin_output()


    def Set_shift_aqusition(): 
        Dwf.dw.FDwfAnalogInChannelEnableSet(Dwf.hdwf, c_int(-1), c_int(1))
        Dwf.dw.FDwfAnalogInChannelOffsetSet(Dwf.hdwf, c_int(-1), c_double(0)) 
        Dwf.dw.FDwfAnalogInChannelRangeSet(Dwf.hdwf, iCH_0, c_double(10))
        Dwf.dw.FDwfAnalogInChannelRangeSet(Dwf.hdwf, iCH_1, c_double(10))
        Dwf.dw.FDwfAnalogInAcquisitionModeSet(Dwf.hdwf, acqmodeScanShift)
        Dwf.dw.FDwfAnalogInConfigure(Dwf.hdwf, c_int(1), c_int(0)) 
        Dwf.dw.FDwfAnalogInFrequencySet(Dwf.hdwf, c_double(200))
        Dwf.dw.FDwfAnalogInBufferSizeSet(Dwf.hdwf,  c_int(SemiMode.buf_size))
        Dwf.dw.FDwfAnalogInConfigure(Dwf.hdwf, c_int(0), c_int(1))

    
    def Set_start_offset_output():
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_double(0))
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, c_double(0))
    
    
    def Set_signal_output():
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, c_bool(True))
        Dwf.dw.FDwfAnalogOutNodeFunctionSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, funcDC)    
    
    
    def Upadate_sample_oCH():
        dxy = 2 * ScanParam.oxy / (ScanParam.resolution - 1)
        d2 = (ImCont.y * dxy) - (ScanParam.oxy) + ScanParam.offset_y
        
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, c_double(d2))    
    
    
    def Primitive_positioning():
        # To change
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_bool(True))
        Dwf.dw.FDwfAnalogOutNodeFunctionSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, funcDC)
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_double(0))
        time.sleep(0.05)
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_double(1))
        time.sleep(0.05)
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_double(2))
        time.sleep(0.05)
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_double(3))
        time.sleep(0.05)
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_double(4))
        time.sleep(0.05)
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_double(5))
        time.sleep(0.05)
        Dwf.dw.FDwfAnalogOutIdleSet(Dwf.hdwf, oCH_A, DwfAnalogOutIdleOffset) 
        Dwf.dw.FDwfAnalogOutIdleSet(Dwf.hdwf, oCH_B, DwfAnalogOutIdleOffset) 
        
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_bool(True))
    
    
    def Set_semi_sin_output():
        oxy = c_double(ScanParam.oxy)
        hzAcq_A = SemiMode.hzAcq[0]
        runtime = 0.5 / hzAcq_A.value
        Dwf.dw.FDwfDeviceAutoConfigureSet(Dwf.hdwf, c_int(3)) # dynamic mode to change parameters
        # Device_semi.Primitive_positioning()
        
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_bool(True))
        Dwf.dw.FDwfAnalogOutNodeFunctionSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, funcSine)
        Dwf.dw.FDwfAnalogOutNodeFrequencySet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, hzAcq_A)
        Dwf.dw.FDwfAnalogOutNodeAmplitudeSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, oxy)
        Dwf.dw.FDwfAnalogOutNodePhaseSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, SemiMode.phase_ch1)
        
        Dwf.dw.FDwfAnalogOutRunSet(Dwf.hdwf, oCH_A, c_double(runtime)) # run once 
        
        Dwf.dw.FDwfAnalogOutConfigure(Dwf.hdwf, oCH_A, c_bool(True))
        
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_double(0)) # check if it is necsesery
                
        time.sleep(2)
        
    
    def Switch_off_output():
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_bool(False))
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, c_bool(False))
    
    
    def Get_conti_data():
        cValid = c_int(0)
        sts = c_byte()
        Dwf.dw.FDwfAnalogInStatus(Dwf.hdwf, c_int(1), byref(sts))
        Dwf.dw.FDwfAnalogInStatusSamplesValid(Dwf.hdwf, byref(cValid))
        
        Dwf.dw.FDwfAnalogInStatusData(Dwf.hdwf, iCH_0, byref(SemiMode.DataCH1), cValid) # get channel 1 data
        Dwf.dw.FDwfAnalogInStatusData(Dwf.hdwf, iCH_1, byref(SemiMode.DataCH2), cValid) # get channel 2 data
        return cValid


            

