import time
import os
import numpy as np
import matplotlib

from pathlib import Path
from dataclasses import dataclass

from src.scan_data import PictureData, DwfData, ScanParam, SemiMode, Logtime
from src.files_operation.general import General_File

class Semi_File:
    
    @staticmethod
    def save_raport():
        WIDTH = 44
        
        name_dir = DwfData.directory + '\\' + DwfData.files
        named_tuple = time.localtime()
        time_string = time.strftime("Date: %Y-%m-%d, Time: %H:%M:%S", named_tuple)
        
        f = open(name_dir + "_Raport_v1.txt", "a", encoding="utf-8")
        
        General_File.save_header(f, time_string)
        
        f.write("Scan mode: \t >> SEMI << " + "\n")
        General_File.save_scan_params(f)
        
        f.write("Scan sample: \t" + str(SemiMode.sample) + "\n")
        f.write("Scan freq: \t" + str(SemiMode.hzAcq[0].value) + "\n")
        f.write("Buf size: \t" + str(SemiMode.buf_size) + "\n")
        f.write("Phaze ch1: \t" + str(SemiMode.phase_ch1) + "\n")
        f.write("Phaze ch2: \t" + str(SemiMode.phase_ch2) + "\n")
        
        General_File.seave_time(f)        
        General_File.save_description(f)
        
        f.close()
    
    
    @staticmethod
    def save_files(time_info):
        if(time_info != ""):
            end_info = "_" + time_info
            Semi_File.save_raport()
        else:
            end_info = ""
            Semi_File.save_raport()
            
        name_dir = DwfData.directory + '\\' + DwfData.files
        named_tuple = time.localtime()
        time_info = time.strftime("%H-%M-%S", named_tuple)
        
        np.savetxt( name_dir + '_CH1_Topo' + end_info + '.dat', PictureData.CHA, fmt="%10.5f", delimiter=";")
        np.savetxt( name_dir + '_CH1_Error' + end_info + '.dat', PictureData.CHB, fmt="%10.5f", delimiter=";")
        
        matplotlib.image.imsave(name_dir + '_CH1_Topo' + end_info + '.png', PictureData.CHA)
        matplotlib.image.imsave(name_dir + '_CH1_Error' + end_info + '.png', PictureData.CHB)

        DwfData.status = 'Saved: ' + DwfData.files + ", at: " + time_info + '  \t\t'