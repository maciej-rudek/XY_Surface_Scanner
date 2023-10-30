from pickle import NONE
import sys
import time

from src.device_conf.dwfconstants import *
from src.device_conf.device_sample import Device_sample
from src.device_conf.device_conti import Device_conti
from src.device_conf.device_semi import Device_semi
from src.scan_data import Dwf, ImCont, SampleMode, ContinuousMode, DwfData, ScanParam, Status
from src.fig_plots import pic

class Device:
    
    def Reset_device():
        Dwf.dw.FDwfAnalogInReset(Dwf.hdwf)
        Dwf.dw.FDwfAnalogOutReset(Dwf.hdwf)
    
    def Configure_setup_mode():
        # Device.Close_ALL()
        # Device.Open_device()
        Device.Reset_device()
        pic.ax_all_visable_off()
        
        if (ScanParam.mode == Status.SAMPLE):
            pic.ax_1256_visable(True)
            Device_sample.Set_sample_aqusition()
            Device_sample.Set_signal_output()
            
        if (ScanParam.mode == Status.CONTINUOUS):
            pic.ax_AB_visable(True)
            # pic.ax_1256_visable(True)
            # Device_conti.Set_continuous_sin_output() # Only for test 
            Device_conti.Set_start_offset_output()
            Device_conti.Set_shift_aqusition()
        
        if (ScanParam.mode == Status.SEMI):
            # pic.ax_C_visable(True)
            pic.ax_AB_visable(True)
            # Device_conti.Set_continuous_sin_output() # Only for test 
            Device_semi.Set_start_offset_output()
            Device_semi.Set_shift_aqusition()
    
    
    def Open_device():
        DwfData.status = "Opening first device"
        # 2nd configuration for Analog Disocovery with 16k analog-in buffer
        Dwf.dw.FDwfDeviceConfigOpen(c_int(-1), c_int(1), byref(Dwf.hdwf)) 
        
        if Dwf.hdwf.value == hdwfNone.value:
            szerr = create_string_buffer(512)
            Dwf.dw.FDwfGetLastErrorMsg(szerr)
            print(str(szerr.value))
            DwfData.logError = "Failed to open device :("
        else:
            time.sleep(2)
            Dwf.rghdwf.append(Dwf.hdwf.value)
            DwfData.status = "First devise is connected"
            Device.Reset_device()


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
