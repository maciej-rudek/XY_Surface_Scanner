
from ctypes import *
import time

from src.scan_data import ImCont, ContinuousMode, DwfData, ScanParam, Status, PictureSCS
from src.device_conf.device import *
from src.device_conf.device_conti import Device_conti


class Mode_continuous:
    
    time_to_watch = 0.0
    
    def Scan():
        WAIT_START = 0.2
        Wait_stop = ( 1 / ContinuousMode.hzAcq[0].value ) * 2
        resolution = ScanParam.resolution
        hzAcq_B = Wait_stop *  resolution 
        
        Device_conti.Get_conti_data()
        
        for i in range(ContinuousMode.buf_size):
            ContinuousMode.f_ch1[i] = float(ContinuousMode.DataCH1[i])
            ContinuousMode.f_ch2[i] = float(ContinuousMode.DataCH2[i])
        
        if (ScanParam.scan == Status.START):
            time.sleep(Wait_stop)
            Mode_continuous.time_to_watch = Mode_continuous.time_to_watch + Wait_stop
            watch = Mode_continuous.time_to_watch
            if (hzAcq_B <= watch):
                ScanParam.scan = Status.STOP
                Mode_continuous.time_to_watch = 0
        else:
            Mode_continuous.time_to_watch = 0
            time.sleep(WAIT_START)
    
    # def join_and_cut():
    #     window = 190
    #     L_space = 10
    #     all_ch2 = np.zeros((nSamples * p_iter))
    #     offset = 0

    #     for i in range(p_iter):
    #         # print(i)
    #         if ( i == 0 ):
    #             all_ch2[0:1000] = tab_ch1[i, 0 : 1000]
    #         else:
    #             krok = 0
    #             while (krok <= nSamples):
    #                 all_sta = (i - 1) * window + L_space + offset
    #                 all_end = all_sta + window
    #                 tab_sta = krok
    #                 tab_end = krok + window
    #                 end_to_nS = nSamples - tab_end
                    
    #                 if(tab_end == (nSamples)):
    #                     krok = 0 
    #                     offset = offset + window
                            
    #                 if ( all_ch2[all_sta:all_end]  ==  tab_ch1[i, tab_sta : tab_end]).all():
    #                     all_ch2[all_sta:all_end + end_to_nS] = tab_ch1[i, tab_sta : tab_end + end_to_nS]
                        
    #                     if ( i > 2 ):
    #                         offset = offset + window
                        
    #                     if( i > 110):
    #                         print("i: ", i, " | k: ", krok, ", all sta: ", all_sta, ", all end: ", all_end, ", tab_s: ", tab_sta, ", tab_e: ", tab_end, ", off: ", offset)
    #                     break
                    
    #                 if(krok == nSamples):
    #                     krok = 0
    #                 else:
    #                     krok = krok + 1
    