import sys
import time

from src.dwfconstants import *
from src.scan_data import Dwf, ImCont, PictureData, SampleMode, ContinuousMode, DwfData, ScanParam, Status, PictureSCS
from src.files_operation import FileOperations



class Device:
    
    def Open_device():
        DwfData.status = "Opening first device"
        Dwf.dw.FDwfDeviceOpen(c_int(-1), byref(Dwf.hdwf))

        if Dwf.hdwf.value == hdwfNone.value:
            szerr = create_string_buffer(512)
            Dwf.dw.FDwfGetLastErrorMsg(szerr)
            print(str(szerr.value))
            DwfData.status = "Failed to open device :("
        else:
            Device.Set_sample_aqusition()
            Device.Set_signal_output()
            time.sleep(2)


    def Check_device():
        if sys.platform.startswith("win"):
            Dwf.dw = cdll.dwf
        elif sys.platform.startswith("darwin"):
            Dwf.dw = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
        else:
            Dwf.dw = cdll.LoadLibrary("libdwf.so")
            
        version = create_string_buffer(16)
        Dwf.dw.FDwfGetVersion(version)
        DwfData.version = str(version.value)
    
    
    def Set_sample_aqusition():
        #set up acquisition 
        Dwf.dw.FDwfAnalogInChannelEnableSet(Dwf.hdwf, c_int(0), c_bool(True))
        Dwf.dw.FDwfAnalogInChannelEnableSet(Dwf.hdwf, c_int(1), c_bool(True))
        Dwf.dw.FDwfAnalogInAcquisitionModeSet(Dwf.hdwf, acqmodeRecord)
        # dwfAnalog InBufferSizeSet(Dwf.hdwf, c_int(SampleMode.sample))
        Dwf.dw.FDwfAnalogInFrequencySet(Dwf.hdwf, SampleMode.hzAcq[0])
        Dwf.dw.FDwfAnalogInRecordLengthSet(Dwf.hdwf, c_double((SampleMode.sample/SampleMode.hzAcq[0].value) - 1)) 
    
    
    def Set_shift_aqusition():
        Dwf.dw.FDwfAnalogInChannelEnableSet(Dwf.hdwf, c_int(-1), c_int(1))
        Dwf.dw.FDwfAnalogInChannelOffsetSet(Dwf.hdwf, c_int(-1), c_double(0)) 
        Dwf.dw.FDwfAnalogInChannelRangeSet(Dwf.hdwf, c_int(0), c_double(5))
        # Dwf.dw.FDwfAnalogInTriggerPositionSet(Dwf.hdwf, c_double(nSamples*4/10/1e6)) # 0 is middle, 4/10 = 10%
        # Dwf.dw.FDwfAnalogInTriggerSourceSet(Dwf.hdwf, c_byte(11)) # 11 = trigsrcExternal1, T1
        Dwf.dw.FDwfAnalogInAcquisitionModeSet(Dwf.hdwf, acqmodeScanShift) #acqmodeScanShift
        Dwf.dw.FDwfAnalogInConfigure(Dwf.hdwf, c_int(1), c_int(0)) 
        Dwf.dw.FDwfAnalogInFrequencySet(Dwf.hdwf, ContinuousMode.hzAcq[0])
        Dwf.dw.FDwfAnalogInBufferSizeSet(Dwf.hdwf, ContinuousMode.buf_size)

        
    def Set_signal_output():
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_bool(True))
        Dwf.dw.FDwfAnalogOutNodeFunctionSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, funcDC)
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, c_bool(True))
        Dwf.dw.FDwfAnalogOutNodeFunctionSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, funcDC)
    
    
    def Set_continuous_sin_output():
        oxy = c_double(ScanParam.oxy)
        hzAcq_A = ContinuousMode.hzAcq[0]
        hzAcq_B = c_double(hzAcq_A / (ScanParam.resolution * 2)) # 2: L->R, R->L in "one" line
        
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_bool(True))
        Dwf.dw.FDwfAnalogOutNodeFunctionSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, funcSine) #sine
        Dwf.dw.FDwfAnalogOutNodeFrequencySet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, hzAcq_A)
        Dwf.dw.FDwfAnalogOutNodeAmplitudeSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, oxy)
        Dwf.dw.FDwfAnalogOutNodePhaseSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, ContinuousMode.phase_ch1)
        
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, c_bool(True))
        Dwf.dw.FDwfAnalogOutNodeFunctionSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, funcSine) #sine
        Dwf.dw.FDwfAnalogOutNodeFrequencySet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, hzAcq_B)
        Dwf.dw.FDwfAnalogOutNodeAmplitudeSet(Dwf.hdwf,oCH_B, AnalogOutNodeCarrier, oxy)
        Dwf.dw.FDwfAnalogOutNodePhaseSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, ContinuousMode.phase_ch2)
        
        Dwf.dw.FDwfAnalogOutConfigure(Dwf.hdwf, oCH_A, c_bool(True))
        Dwf.dw.FDwfAnalogOutConfigure(Dwf.hdwf, oCH_B, c_bool(True))
        # print(dwf.FDwfAnalogOutStatus(hdwf, c_int(0), byref(sts)))

    def Update_freqency():
        if(SampleMode.hzAcq[0] != SampleMode.hzAcq[1]):
            SampleMode.hzAcq[1] = SampleMode.hzAcq[0]
            Dwf.dw.FDwfAnalogInFrequencySet(Dwf.hdwf, SampleMode.hzAcq[0])
            Dwf.dw.FDwfAnalogInRecordLengthSet(Dwf.hdwf, c_double((SampleMode.sample/SampleMode.hzAcq[0].value) - 1))
            DwfData.logError = "Data frequency success updated in device"
            

    def Upadate_sample_oCH():
        dxy = 2 * ScanParam.oxy / (ScanParam.resolution - 1)

        d1 = (ImCont.x * dxy) - (ScanParam.oxy) + ScanParam.offset_x
        d2 = (ImCont.y * dxy) - (ScanParam.oxy) + ScanParam.offset_y
        
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, oCH_A, AnalogOutNodeCarrier, c_double(d1))
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, oCH_B, AnalogOutNodeCarrier, c_double(d2))
        

    def Start_osciloscope():
        csamples = 0

        Dwf.dw.FDwfAnalogInConfigure(Dwf.hdwf, c_int(0), c_int(1))

        while csamples < SampleMode.sample:
            Dwf.dw.FDwfAnalogInStatus(Dwf.hdwf, c_int(1), byref(Dwf.sts))
            if csamples == 0 and (Dwf.sts == DwfStateConfig or Dwf.sts == DwfStatePrefill or Dwf.sts == DwfStateArmed) :
                continue # Acquisition not yet started.

            Dwf.dw.FDwfAnalogInStatusRecord(Dwf.hdwf, byref(DwfData.cAvailable), byref(DwfData.cLost), byref(DwfData.cCorrupted))
            
            csamples += DwfData.cLost.value

            if DwfData.cLost.value :
                DwfData.fLost = 1
            if DwfData.cCorrupted.value :
                DwfData.fCorrupted = 1

            if DwfData.cAvailable.value==0 :
                continue

            if csamples+DwfData.cAvailable.value > SampleMode.sample :
                DwfData.cAvailable = c_int(SampleMode.sample-csamples)
            
            Dwf.dw.FDwfAnalogInStatusData(Dwf.hdwf, c_int(0), byref(SampleMode.DataCH1, sizeof(c_double)*csamples), DwfData.cAvailable) # get channel 1 data
            Dwf.dw.FDwfAnalogInStatusData(Dwf.hdwf, c_int(1), byref(SampleMode.DataCH2, sizeof(c_double)*csamples), DwfData.cAvailable) # get channel 2 data
            csamples += DwfData.cAvailable.value
            
            if(ScanParam.scan == Status.EXIT):
                break

            if (DwfData.logStat == Status.YES):
                local_time = "[" + time.strftime("%H:%M:%S",time.localtime()) + "] "
                if DwfData.fLost:
                    DwfData.logError = local_time + "Samples were lost! Reduce frequency"
                    DwfData.logStat = Status.NO
                if DwfData.fCorrupted:
                    DwfData.logError = local_time + "Samples could be corrupted! Reduce frequency"
                    DwfData.logStat = Status.NO



