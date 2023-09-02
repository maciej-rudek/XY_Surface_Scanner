
from ctypes import *
from matplotlib import pyplot as plt
import time

from src.scan_data import ImCont, ContinuousMode, DwfData, ScanParam, Status, PictureSCS
from src.menu.menu_controll import MenuControll 
from src.files_operation import FileOperations
from src.device_conf.device import *
from src.device_conf.device import Device
from src.scan_mode.sample import Mode_sample


class Mode_continuous:
    
    def Colect_Data():
        Wait_time= ( 1/ContinuousMode.hzAcq[0] ) * 2
        Device.Get_conti_data
        time.sleep(Wait_time)