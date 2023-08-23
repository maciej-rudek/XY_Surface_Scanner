import sys
import time

from src.dwfconstants import *
from src.scan_data import Dwf, ImCont, PictureData, ScanSample, DwfData, ScanParam, Status, PictureSCS
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
        # dwfAnalogInBufferSizeSet(Dwf.hdwf, c_int(ScanSample.sample))
        Dwf.dw.FDwfAnalogInFrequencySet(Dwf.hdwf, DwfData.hzAcq[0])
        Dwf.dw.FDwfAnalogInRecordLengthSet(Dwf.hdwf, c_double((ScanSample.sample/DwfData.hzAcq[0].value) - 1)) 
        
        
    def Set_signal_output():
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, c_int(0), AnalogOutNodeCarrier, c_bool(True))
        Dwf.dw.FDwfAnalogOutNodeFunctionSet(Dwf.hdwf, c_int(0), AnalogOutNodeCarrier, funcDC)
        Dwf.dw.FDwfAnalogOutNodeEnableSet(Dwf.hdwf, c_int(1), AnalogOutNodeCarrier, c_bool(True))
        Dwf.dw.FDwfAnalogOutNodeFunctionSet(Dwf.hdwf, c_int(1), AnalogOutNodeCarrier, funcDC)


    def start_osciloscope():
        csamples = 0

        Dwf.dw.FDwfAnalogInConfigure(Dwf.hdwf, c_int(0), c_int(1))

        while csamples < ScanSample.sample:
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

            if csamples+DwfData.cAvailable.value > ScanSample.sample :
                DwfData.cAvailable = c_int(ScanSample.sample-csamples)
            
            Dwf.dw.FDwfAnalogInStatusData(Dwf.hdwf, c_int(0), byref(ScanSample.DataCH1, sizeof(c_double)*csamples), DwfData.cAvailable) # get channel 1 data
            Dwf.dw.FDwfAnalogInStatusData(Dwf.hdwf, c_int(1), byref(ScanSample.DataCH2, sizeof(c_double)*csamples), DwfData.cAvailable) # get channel 2 data
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



