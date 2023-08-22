import sys
import time

from src.dwfconstants import *
from src.scan_data import Dwf, ImCont, PictureData, ScanSample, DwfData, ScanParam, Status, PictureSCS
from src.files_operation import FileOperations

# from XY_scanner import start_osciloscope

#declare ctype variables
hdwf = c_int()
sts = c_byte()

#open device

class Device:

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
        # print(DwfData.version)
    
    def Set_sample_aqusition():
        #set up acquisition 
        Dwf.dw.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_bool(True))
        Dwf.dw.FDwfAnalogInChannelEnableSet(hdwf, c_int(1), c_bool(True))
        Dwf.dw.FDwfAnalogInAcquisitionModeSet(hdwf, acqmodeRecord)
        # dwfAnalogInBufferSizeSet(hdwf, c_int(ScanSample.sample))
        Dwf.dw.FDwfAnalogInFrequencySet(hdwf, DwfData.hzAcq[0])
        Dwf.dw.FDwfAnalogInRecordLengthSet(hdwf, c_double((ScanSample.sample/DwfData.hzAcq[0].value) - 1)) 

        Dwf.dw.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_bool(True))
        Dwf.dw.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), AnalogOutNodeCarrier, funcDC)
        Dwf.dw.FDwfAnalogOutNodeEnableSet(hdwf, c_int(1), AnalogOutNodeCarrier, c_bool(True))
        Dwf.dw.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(1), AnalogOutNodeCarrier, funcDC)




