import os
import time
import numpy as np

from enum import Enum
from ctypes import *
from XY_Surface_Scanner.src.device_configuration import Device
from src.scan_data import Dwf, ImCont, SampleMode, ContinuousMode, Status, ScanParam, DwfData, Logtime, PictureData, PictureSCS
from src.files_operation import FileOperations


class Mode_sample:
    
    stan = 0
    
    @staticmethod
    def Reset_Scan():
        Mode_sample.stan = 0
        resolution = ScanParam.resolution
        ImCont.dir = 0
        ImCont.x = 0
        ImCont.y = 0
        ImCont.oY = 0
        PictureData.line = 0
        PictureData.CH1 = np.zeros((resolution, resolution))
        PictureData.CH2 = np.zeros((resolution, resolution))
        PictureData.CH3 = np.zeros((resolution, resolution))
        PictureData.CH4 = np.zeros((resolution, resolution))
    
    @staticmethod
    def Scan():
        resolution = ScanParam.resolution
        
        Device.Update_freqency()

        for i in range(SampleMode.sample):
            SampleMode.f_ch1[i] = float(SampleMode.DataCH1[i])
            SampleMode.f_ch2[i] = float(SampleMode.DataCH2[i])
        
        maks = SampleMode.sample
        marg = 0.1 * maks

        # PictureData.CH2[y, ImCont.x] = np.mean(SampleMode.f_ch2) 

        if (ScanParam.scan == Status.START):
            if (Mode_sample.stan == 0):
                if (ImCont.x == (resolution)):
                    Mode_sample.stan = 1
                else:
                    ImCont.dir = 0
                    PictureData.CH1[ImCont.y, ImCont.x] = np.mean(SampleMode.f_ch1[int(marg):int(maks-marg)])
                    PictureData.CH2[ImCont.y, ImCont.x] = np.mean(SampleMode.f_ch2[int(marg):int(maks-marg)]) 
                ImCont.x = ImCont.x + 1
                
            elif (Mode_sample.stan == 1):
                ImCont.x = ImCont.x - 2
                Mode_sample.stan = 2
                # if (parametrImCont.y['tImCont.ype'] == 'snake'):
                # ImCont.y = ImCont.y + 1

            elif (Mode_sample.stan == 2):
                if (ImCont.x == -1):
                    ImCont.x = 0
                    Mode_sample.stan = 3
                else:
                    ImCont.dir = 1
                    PictureData.CH3[ImCont.y, ImCont.x] = np.mean(np.mean(SampleMode.f_ch1[int(marg):int(maks-marg)]))
                    PictureData.CH4[ImCont.y, ImCont.x] = np.mean(SampleMode.f_ch2[int(marg):int(maks-marg)]) 
                ImCont.x = ImCont.x - 1
               
                    
            elif (Mode_sample.stan == 3):                 
                ImCont.x = ImCont.x + 1
                ImCont.y = ImCont.y + 1
                ImCont.oY = ImCont.oY + 1
                PictureData.line = PictureData.line + 1
                if(ImCont.oY == resolution):
                    FileOperations.save_manager_files()
                    ImCont.oY = 0
                    # TODO: Wait for action from user - befor stop 
                    ScanParam.scan = Status.STOP
                Mode_sample.stan = 0
                # print(PictureData.line, old_PictureData.line)
                # Tutaj dodac kalkulacje srredniej dla X,Y dla kazdego kanału i zamiana 0 na srednia z poprzedniej linii pomiarowej

        else:
            ImCont.dir = 0
            Mode_sample.stan = 0
            ImCont.x = 0
            ImCont.y = 0
            ImCont.oY = 0
            PictureData.line = 0
            PictureData.CH1 = np.zeros((resolution, resolution))
            PictureData.CH2 = np.zeros((resolution, resolution))
            PictureData.CH3 = np.zeros((resolution, resolution))
            PictureData.CH4 = np.zeros((resolution, resolution))
        
        if ((PictureData.line > 0) and (PictureData.line < resolution) and (PictureSCS.interpolate == Status.YES) ):
            A = PictureData.CH1[PictureData.line,0:resolution]
            B = PictureData.CH2[PictureData.line,0:resolution]

            # (c*np.mean(w)+(np.max(w)-np.min(w))-abs((np.min(w))) 
            # PictureData.CH1[0:resolution,(PictureData.line+1):resolution] = np.mean(A)
            #np.random.rand(((resolution - (PictureData.line+1)),resolution)) *  (np.mean(A)+(np.max(A)-np.min(A))-abs((np.min(A))))
            PictureData.CH1[(PictureData.line+1):resolution,0:resolution] = np.resize(A,((resolution - (PictureData.line+1)),resolution)) 
            PictureData.CH2[(PictureData.line+1):resolution,0:resolution] = np.resize(B,((resolution - (PictureData.line+1)),resolution)) 
            A = PictureData.CH3[PictureData.line,0:resolution]
            B = PictureData.CH4[PictureData.line,0:resolution]
            PictureData.CH3[(PictureData.line+1):resolution,0:resolution] = np.resize(A,((resolution - (PictureData.line+1)),resolution)) 
            PictureData.CH4[(PictureData.line+1):resolution,0:resolution] = np.resize(B,((resolution - (PictureData.line+1)),resolution)) 
        else:
            PictureData.CH1[(PictureData.line+1):resolution,0:resolution] = 0 
            PictureData.CH2[(PictureData.line+1):resolution,0:resolution] = 0
            PictureData.CH3[(PictureData.line+1):resolution,0:resolution] = 0
            PictureData.CH4[(PictureData.line+1):resolution,0:resolution] = 0
        #time.sleep(0.02)
    