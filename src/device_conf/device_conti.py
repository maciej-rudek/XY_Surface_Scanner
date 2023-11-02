import sys
import time

from src.device_conf.dwfconstants import *
from src.scan_data import Dwf, ImCont, SampleMode, ContinuousMode, DwfData, ScanParam, Status
from src.scan_mode.special import Once

class Device_conti:
    
    @Once.Run_once
    def First_configuration():
        Device_conti.Set_shift_aqusition()
        Device_conti.Set_continuous_sin_output()


    def Set_shift_aqusition(): 
        hzAcq_A = ContinuousMode.hzAcq[0]
        iterations = float(ScanParam.resolution)
        frequency = hzAcq_A.value * iterations * 2
        
        Dwf.dw.FDwfAnalogInChannelEnableSet(Dwf.hdwf, c_int(-1), c_int(1))
        Dwf.dw.FDwfAnalogInChannelOffsetSet(Dwf.hdwf, c_int(-1), c_double(0)) 
        Dwf.dw.FDwfAnalogInChannelRangeSet(Dwf.hdwf, iCH_0, c_double(10))
        Dwf.dw.FDwfAnalogInChannelRangeSet(Dwf.hdwf, iCH_1, c_double(10))
        Dwf.dw.FDwfAnalogInAcquisitionModeSet(Dwf.hdwf, acqmodeScanShift)
        Dwf.dw.FDwfAnalogInConfigure(Dwf.hdwf, c_int(1), c_int(0)) 
        Dwf.dw.FDwfAnalogInFrequencySet(Dwf.hdwf, c_double(frequency))
        Dwf.dw.FDwfAnalogInBufferSizeSet(Dwf.hdwf,  c_int(ContinuousMode.buf_size))
        Dwf.dw.FDwfAnalogInConfigure(Dwf.hdwf, c_int(0), c_int(1))

    
    def Set_start_offset_output():
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_double(0))
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, c_double(0))
        
    
    def Set_continuous_sin_output():
        oxy = c_double(ScanParam.oxy)
        resolution = ScanParam.resolution
        hzAcq_A = ContinuousMode.hzAcq[0]
        hzAcq_B = c_double(hzAcq_A.value / ( resolution * 2 ) ) # 2: L->R, R->L in "one" line
        runtime = (1 / hzAcq_B.value) / 2
        Dwf.dw.FDwfDeviceAutoConfigureSet(Dwf.hdwf, c_int(3)) # dynamic mode to change parameters
        
        # FAST scan - X
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_bool(True))
        if(ScanParam.x_scan == Status.SINUS):
            Dwf.dw.FDwfAnalogOutNodeFunctionSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, funcSine)
        if(ScanParam.x_scan == Status.TRIANGLE):
            Dwf.dw.FDwfAnalogOutNodeFunctionSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, funcTriangle)

        Dwf.dw.FDwfAnalogOutNodeFrequencySet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, hzAcq_A)
        Dwf.dw.FDwfAnalogOutNodeAmplitudeSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, oxy)
        Dwf.dw.FDwfAnalogOutNodePhaseSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, ContinuousMode.phase_ch1)
        
        # SLOW scan - Y
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, c_bool(True))
        Dwf.dw.FDwfAnalogOutNodeFunctionSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, funcTriangle)
        Dwf.dw.FDwfAnalogOutNodeFrequencySet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, hzAcq_B)
        Dwf.dw.FDwfAnalogOutNodeAmplitudeSet(Dwf.hdwf,oCH_B, AnalogOutNodeCarrier, oxy)
        Dwf.dw.FDwfAnalogOutNodePhaseSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, ContinuousMode.phase_ch2)
        
        Dwf.dw.FDwfAnalogOutRunSet(Dwf.hdwf, oCH_A, c_double(runtime)) # run once 
        Dwf.dw.FDwfAnalogOutRunSet(Dwf.hdwf, oCH_B, c_double(runtime)) # run once 
        
        Dwf.dw.FDwfAnalogOutConfigure(Dwf.hdwf, oCH_A, c_bool(True))
        Dwf.dw.FDwfAnalogOutConfigure(Dwf.hdwf, oCH_B, c_bool(True))
        
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
        
        Dwf.dw.FDwfAnalogInStatusData(Dwf.hdwf, iCH_0, byref(ContinuousMode.DataCH1), cValid) # get channel 1 data
        Dwf.dw.FDwfAnalogInStatusData(Dwf.hdwf, iCH_1, byref(ContinuousMode.DataCH2), cValid) # get channel 2 data
        return cValid.value



            

