import os
import time
import numpy as np

from enum import Enum
from ctypes import *
from src.scan_data import ImCont, SampleMode, ContinuousMode, Status, ScanParam, SemiMode, DwfData, PictureData, PictureSCS
from src.files_operation.operation import File_Operation
from src.device_conf.device import Device


class MenuParams:

## DATA:

    @staticmethod
    def param_sample(data_params):
        """Nr of Samples [200-20000]"""
        if(ScanParam.mode == Status.SAMPLE):
            SampleMode.sample = int(data_params) % 20000
            SampleMode.DataCH1 = (c_double*SampleMode.sample)()
            SampleMode.DataCH2= (c_double*SampleMode.sample)()
            SampleMode.f_ch1 = np.arange(SampleMode.sample, dtype=float)
            SampleMode.f_ch2 = np.arange(SampleMode.sample, dtype=float)
            
        if(ScanParam.mode == Status.CONTINUOUS):
            ContinuousMode.DataCH1 = (c_double*SampleMode.sample)()
            ContinuousMode.DataCH2= (c_double*SampleMode.sample)()
            ContinuousMode.f_ch1 = np.arange(SampleMode.sample, dtype=float)
            ContinuousMode.f_ch2 = np.arange(SampleMode.sample, dtype=float)
        
    @staticmethod
    def param_area(data_params):
        """Scan Area [1-100] """
        ScanParam.area = int(data_params)
        ScanParam.oxy = 5 * float(ScanParam.area/100)

    @staticmethod
    def param_res(data_params):
        """Resolution [50-500] """
        ScanParam.resolution = int(data_params)
        if(ScanParam.mode == Status.CONTINUOUS):
            ContinuousMode.v_ch1 = np.arange(ScanParam.resolution * 2, dtype=float)
            ContinuousMode.v_ch2 = np.arange(ScanParam.resolution * 2, dtype=float)

    @staticmethod
    def param_freq(data_params):
        """Scan Frequency """
        
        if(ScanParam.mode == Status.SAMPLE):
            dana = (int(data_params) % 2000) * 1000
            SampleMode.hzAcq[0] = c_double(dana)
        if(ScanParam.mode == Status.CONTINUOUS):
            dana = float(data_params)
            ContinuousMode.hzAcq[0] = c_double(dana)
        if(ScanParam.mode == Status.SEMI):
            dana = float(data_params)
            SemiMode.hzAcq[0] = c_double(dana)

    @staticmethod
    def param_save(data_params):
        """Save picture [yes, no]"""
        PictureData.save = Status(data_params)
    
    @staticmethod
    def param_stat(data_params):
        """____"""
        ScanParam.scan = Status(data_params)
    
    @staticmethod
    def param_oxy(data_params):
        """____"""
        ScanParam.oxy = float(data_params)
        ScanParam.area = int((ScanParam.oxy/5) * 100)

    @staticmethod
    def param_dx(data_params):
        """____"""
        ImCont.x = float(data_params)
    
    @staticmethod
    def param_dy(data_params):
        """____"""
        ImCont.y = float(data_params)
    
    @staticmethod
    def param_phase1(data_params):
        """oCH 1 - phase shift"""
        if(ScanParam.mode != Status.SAMPLE):
            ContinuousMode.phase_ch1 = c_double(data_params)
        else:
            DwfData.logError = "NO Continuous mode ON !"

    @staticmethod
    def param_phase2(data_params):
        """oCH 2 - phase shift"""
        if(ScanParam.mode != Status.SAMPLE):
            ContinuousMode.phase_ch2 = c_double(data_params)
        else:
            DwfData.logError = "NO continuous or semi mode ON !"
    
    @staticmethod
    def param_x(data_params):
        """x - type of scan [sinus, trangle]"""
        ScanParam.x_scan = Status(data_params)
        
## INSTRUCTIONS:

    @staticmethod
    def param_scan(data_params):
        """Scan: Start"""
        named_tuple = time.localtime()
        time_info = time.strftime("%H-%M-%S", named_tuple)
        DwfData.logTime.start = time_info
        ScanParam.scan = Status.START

    @staticmethod
    def param_stop(data_params):
        """Scan: Stop"""
        ScanParam.scan = Status.STOP

    @staticmethod
    def param_save(data_params):
        """File: Save"""
        named_tuple = time.localtime()
        time_info = time.strftime("%H-%M-%S", named_tuple)
        File_Operation.save_manager_files(time_info)
        # ScanParam.scan = Status.SAVE

    @staticmethod
    def param_exit(data_params):
        """Exit program"""
        ScanParam.scan = Status.EXIT
    
    @staticmethod
    def param_inter(data_params):
        """Interpolate picture [yes, no]"""
        PictureSCS.interpolate = Status(data_params)

    @staticmethod
    def param_log(data_params):
        """Show Logs from Analog Discovery 2 [yes, no]"""
        DwfData.logStat = Status(data_params)
    
    @staticmethod
    def param_mode(data_params):
        """Scan Modes [sample, semi, continuous]"""
        ScanParam.mode_new = Status(data_params)
        DwfData.clear_menu = True

