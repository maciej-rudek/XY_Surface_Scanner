import time
import os
import numpy as np
import matplotlib

from pathlib import Path
from dataclasses import dataclass

from src.scan_data import PictureData, DwfData

class FileOperations:
    
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
            FileOperations.directory_manage()


    @staticmethod
    def check_files():
        while True:
            i = int(DwfData.files)
            path = DwfData.directory + "\\" + DwfData.files + 'CH1_Topo' + '.txt'
            if os.path.isfile(path):
                i = i + 1
                DwfData.files = f"{i:03}"
            else:
                break           
        # print(os.path.isfile(DwfData.directory + "\\000_time_string.txt"))
        # print(os.path.abspath(DwfData.directory))


    @staticmethod
    def save_files():
        name_dir = DwfData.directory + '\\' + DwfData.files
        named_tuple = time.localtime()
        time_string = time.strftime("%Y-%m-%d_%H-%M-%S", named_tuple)
        
        np.savetxt( name_dir + 'CH1_Topo' + '.txt', PictureData.CH1, fmt="%10.5f", delimiter=";")
        np.savetxt( name_dir + 'CH1_Error' + '.txt', PictureData.CH2, fmt="%10.5f", delimiter=";")
        np.savetxt( name_dir + 'CH2_Topo' + '.txt', PictureData.CH3, fmt="%10.5f", delimiter=";")
        np.savetxt( name_dir + 'CH2_Error' + '.txt', PictureData.CH4, fmt="%10.5f", delimiter=";")
        
        matplotlib.image.imsave(name_dir + 'CH1_Topo' + '.png', PictureData.CH1)
        matplotlib.image.imsave(name_dir + 'CH1_Error' + '.png', PictureData.CH2)
        matplotlib.image.imsave(name_dir + 'CH2_Topo' + '.png', PictureData.CH3)
        matplotlib.image.imsave(name_dir + 'CH2_Error' + '.png', PictureData.CH4)

        DwfData.logError = 'ALL files saved: ' + time_string + ' ]:-> '
    
    
    @staticmethod
    def save_manager_files():
        FileOperations.directory_manage()
        FileOperations.check_files()
        FileOperations.save_files()
