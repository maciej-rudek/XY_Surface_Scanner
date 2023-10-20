import time
import os
import numpy as np
import matplotlib

from pathlib import Path
from dataclasses import dataclass

from src.scan_data import PictureData, DwfData, ScanParam, SampleMode, Logtime

class General_File:
    
    WIDTH = 44
    
    @staticmethod
    def save_header(f, time_string):
        
        
        f.write("=" * General_File.WIDTH + "\n")
        f.write("        ┏  ┏┓         ┳┓           ┓      \n") 
        f.write("        ┃  ┗┓┏┏┓┏┓    ┣┫┏┓┏┓┏┓┏┓╋  ┃      \n")
        f.write("        ┗  ┗┛┗┗┻┛┗    ┛┗┗┻┣┛┗┛┛ ┗  ┛      \n")
        f.write("                          ┛               \n")
        #   tmplr font 
        f.write("" + time_string + "\n")
        f.write("=" * General_File.WIDTH + "\n")
    
    
    def save_scan_params(f):
        f.write("=" * General_File.WIDTH + "\n")
        f.write("Scan sample: \t" + str(SampleMode.sample) + "\n")
        f.write("Resolution: \t"  + str(ScanParam.resolution) + " px \n")
        f.write("Scan area: \t"  + str(ScanParam.area) + " % \n")
        f.write("Scan area: \t"  + str(ScanParam.oxy) + " V \n")
        f.write("Offset X: \t"  + str(ScanParam.offset_x) + "\n")
        f.write("Offset Y: \t"  + str(ScanParam.offset_y) + "\n")
    
    def seave_time(f):
        f.write("=" * General_File.WIDTH + "\n")
        f.write("Time start: \t"  + str(Logtime.start) + "\n")
        f.write("Time end: \t"  + str(Logtime.end) + "\n")
        f.write("Duration: \t"  + str(Logtime.duration) + "\n")
       
    def save_description(f):
        f.write("=" * General_File.WIDTH + "\n")
        f.write("File title: \t" + str(DwfData.title) + "\n")
        f.write("Directory: \t" + str(DwfData.directory) + "\n")
        f.write("File nr.: \t" + str(DwfData.files) + "\n")