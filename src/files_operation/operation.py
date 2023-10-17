import time
import os
import numpy as np
import matplotlib

from pathlib import Path
from dataclasses import dataclass

from src.scan_data import PictureData, DwfData, ScanParam, SampleMode, Logtime, Status
from src.files_operation.semi_file import Semi_File
from src.files_operation.sample_file import Sample_File
from src.files_operation.continuous_file import Continuous_File
from src.files_operation.menage import File_Menage

class File_Operation:      

    @staticmethod
    def save_manager_files(time_info = ""):
        File_Menage.directory_manage()
        File_Menage.check_files(time_info)
        
        if (ScanParam.mode == Status.SAMPLE):       # Working fine
            Sample_File.save_files(time_info)
        if (ScanParam.mode == Status.CONTINUOUS):   # Not working
            Continuous_File.save_files(time_info)
        if (ScanParam.mode == Status.SEMI):         # In progress
            Semi_File.save_files(time_info)
