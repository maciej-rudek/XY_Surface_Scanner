import sys
import time

from src.device_conf.dwfconstants import *
from src.device_conf.device_sample import Device_sample
from src.device_conf.device_conti import Device_conti
from src.scan_data import Dwf, ImCont, SampleMode, ContinuousMode, DwfData, ScanParam, Status


class Device:
    
    def Configure_setup_mode():
        if (ScanParam.mode == Status.SAMPLE):
            Device_sample.Set_sample_aqusition()
            Device_sample.Set_signal_output()
            
        if (ScanParam.mode == Status.CONTINUOUS):
            # Dwf.rghdwf.append(Dwf.hdwf.value)
            Device_conti.Set_continuous_sin_output()
            Device_conti.Set_shift_aqusition()
            # Dwf.dw.FDwfAnalogInConfigure(Dwf.hdwf, c_int(0), c_int(1))
    
    
    def Open_device():
        DwfData.status = "Opening first device"
        Dwf.dw.FDwfDeviceOpen(c_int(-1), byref(Dwf.hdwf))

        if Dwf.hdwf.value == hdwfNone.value:
            szerr = create_string_buffer(512)
            Dwf.dw.FDwfGetLastErrorMsg(szerr)
            print(str(szerr.value))
            DwfData.status = "Failed to open device :("
        else:
            time.sleep(2)
            Dwf.rghdwf.append(Dwf.hdwf.value)


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
    
    
    def Close_ALL():
        Dwf.dw.FDwfAnalogOutConfigure(Dwf.hdwf, c_int(0), c_bool(False))
        Dwf.dw.FDwfDeviceCloseAll()
