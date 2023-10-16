import time
import os
import numpy as np
import matplotlib

from pathlib import Path
from dataclasses import dataclass

from src.scan_data import PictureData, DwfData, ScanParam, SampleMode, Logtime, Status
from src.files_operation.semi import Semi_File
from src.files_operation.sample import Sample_File
from src.files_operation.continuous import Continuous_File

class File_Operation:   
    
    @staticmethod
    def check_time():
        return 0


    @staticmethod
    def directory_manage():
        named_tuple = time.localtime()
        date_info = time.strftime("%Y%m%d", named_tuple)
        time_info = time.strftime("%H-%M-%S", named_tuple)
        DwfData.logTime.end = time_info
        DwfData.directory = str(date_info[2:8] + "_" + DwfData.title)
        
        if os.path.isdir(DwfData.directory):
            DwfData.logError = "Directory: " + DwfData.directory + " is existing."
        else:
            os.mkdir(DwfData.directory)
            DwfData.logError = "New directory created: " + DwfData.directory
            File_Operation.directory_manage()


    @staticmethod
    def check_files(time_info):
        if(time_info == ""):
            while True:
                path = DwfData.directory + "\\" + DwfData.files + '_CH1_Topo' + '.dat'
                if os.path.isfile(path):
                    i = int(DwfData.files)
                    i = i + 1
                    DwfData.files = f"{i:03}"
                else:
                    break     
        else:
            i = int(DwfData.files)   
            DwfData.files = f"{i:03}"
            
        # print(os.path.isfile(DwfData.directory + "\\000_time_string.txt"))
        # print(os.path.abspath(DwfData.directory))   

    @staticmethod
    def save_manager_files(time_info = ""):
        File_Operation.directory_manage()
        File_Operation.check_files(time_info)
        
        if (ScanParam.mode == Status.SAMPLE):       # Working fine
            Sample_File.save_files(time_info)
        if (ScanParam.mode == Status.CONTINUOUS):   # Not working
            Continuous_File.save_files(time_info)
        if (ScanParam.mode == Status.SEMI):         # In progress
            Semi_File.save_files(time_info)
