import sys
import time

from src.device_conf.dwfconstants import *
from src.scan_data import Dwf, ImCont, SampleMode, ContinuousMode, DwfData, ScanParam, Status


class Device_conti:

    def Set_shift_aqusition():
        Dwf.dw.FDwfAnalogInChannelEnableSet(Dwf.hdwf, c_int(-1), c_int(1))
        Dwf.dw.FDwfAnalogInChannelOffsetSet(Dwf.hdwf, c_int(-1), c_double(0)) 
        Dwf.dw.FDwfAnalogInChannelRangeSet(Dwf.hdwf, c_int(0), c_double(5))
        # Dwf.dw.FDwfAnalogInTriggerPositionSet(Dwf.hdwf, c_double(nSamples*4/10/1e6)) # 0 is middle, 4/10 = 10%
        # Dwf.dw.FDwfAnalogInTriggerSourceSet(Dwf.hdwf, c_byte(11)) # 11 = trigsrcExternal1, T1
        Dwf.dw.FDwfAnalogInAcquisitionModeSet(Dwf.hdwf, acqmodeScanShift) #acqmodeScanShift
        Dwf.dw.FDwfAnalogInConfigure(Dwf.hdwf, c_int(1), c_int(0)) 
        Dwf.dw.FDwfAnalogInFrequencySet(Dwf.hdwf, c_double(200))
        Dwf.dw.FDwfAnalogInBufferSizeSet(Dwf.hdwf, c_int(ContinuousMode.buf_size))
    
    
    def Set_continuous_sin_output():
        oxy = c_double(ScanParam.oxy)
        resolution = ScanParam.resolution
        hzAcq_A = ContinuousMode.hzAcq[0]
        hzAcq_B = c_double(hzAcq_A.value / resolution * 2) # 2: L->R, R->L in "one" line
        
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_bool(True))
        Dwf.dw.FDwfAnalogOutNodeFunctionSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_int(1)) #sine
        Dwf.dw.FDwfAnalogOutNodeFrequencySet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_double(0.01))
        Dwf.dw.FDwfAnalogOutNodeAmplitudeSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, oxy)
        Dwf.dw.FDwfAnalogOutNodePhaseSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, ContinuousMode.phase_ch1)
        
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, c_bool(True))
        Dwf.dw.FDwfAnalogOutNodeFunctionSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, c_int(1)) #sine
        Dwf.dw.FDwfAnalogOutNodeFrequencySet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, c_double(1))
        Dwf.dw.FDwfAnalogOutNodeAmplitudeSet(Dwf.hdwf,oCH_B, AnalogOutNodeCarrier, oxy)
        Dwf.dw.FDwfAnalogOutNodePhaseSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, ContinuousMode.phase_ch2)
        
        Dwf.dw.FDwfAnalogOutConfigure(Dwf.hdwf, oCH_A, c_bool(True))
        Dwf.dw.FDwfAnalogOutConfigure(Dwf.hdwf, oCH_B, c_bool(True))
        
        time.sleep(2)
        
        Dwf.dw.FDwfAnalogInConfigure(Dwf.hdwf, c_int(0), c_int(1))
    
    
    def Get_conti_data():
        Dwf.dw.FDwfAnalogInStatus(Dwf.hdwf, c_int(1), byref(c_byte()))
        Dwf.dw.FDwfAnalogInStatusSamplesValid(Dwf.hdwf, byref(c_int(0)))
        
        Dwf.dw.FDwfAnalogInStatusData(Dwf.hdwf, iCH_1, byref(ContinuousMode.DataCH1), c_int(0)) # get channel 1 data
        Dwf.dw.FDwfAnalogInStatusData(Dwf.hdwf, iCH_2, byref(ContinuousMode.DataCH2), c_int(0)) # get channel 2 data



            

