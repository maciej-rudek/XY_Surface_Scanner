import matplotlib
import threading
import time
import sys
import numpy as np
import os

from ctypes import *
from src.dwfconstants import *
from matplotlib import pyplot as plt
from matplotlib import animation

from src.scan_data import Dwf, ImCont, PictureData, SampleMode, DwfData, ScanParam, Status, PictureSCS
from src.menu.menu_controll import MenuControll 
from src.files_operation import FileOperations
from src.device_configuration import Device #, start_osciloscope #Check_device

np.random.seed(19680801)

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
gs = fig.add_gridspec(2,4)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax5 = fig.add_subplot(gs[0, 2])
ax6 = fig.add_subplot(gs[0, 3])
ax3 = fig.add_subplot(gs[1, :], label="1")
ax4 = fig.add_subplot(gs[1, :], label="2", frame_on=False)
x = np.linspace(0, 10*np.pi, 100)
y = np.sin(x)
line1, = ax4.plot(x, y, 'b-')


def Start_AD2():
    stan = 0

    resolution = ScanParam.resolution

    while (ScanParam.scan != Status.EXIT):
        
        dxy = 2 * ScanParam.oxy / (resolution - 1)

        d1 = (ImCont.x * dxy)  - (ScanParam.oxy)
        d2 = (ImCont.y * dxy)  - (ScanParam.oxy)
        
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, c_int(0), AnalogOutNodeCarrier, c_double(d1))
        Dwf.dw.FDwfAnalogOutNodeOffsetSet(Dwf.hdwf, c_int(1), AnalogOutNodeCarrier, c_double(d2))

        Device.start_osciloscope()

        if(SampleMode.hzAcq[0] != SampleMode.hzAcq[1]):
            SampleMode.hzAcq[1] = SampleMode.hzAcq[0]
            Dwf.dw.FDwfAnalogInFrequencySet(Dwf.hdwf, SampleMode.hzAcq[0])
            Dwf.dw.FDwfAnalogInRecordLengthSet(Dwf.hdwf, c_double((SampleMode.sample/SampleMode.hzAcq[0].value) - 1))
            DwfData.logError = "Data frequency success updated in device"

        for i in range(SampleMode.sample):
            SampleMode.f_ch1[i] = float(SampleMode.DataCH1[i])
            SampleMode.f_ch2[i] = float(SampleMode.DataCH2[i])
        
        maks = SampleMode.sample
        marg = 0.1 * maks
        
        if(ScanParam.scan == Status.EXIT):
            break

        # PictureData.CH2[y, ImCont.x] = np.mean(SampleMode.f_ch2) 

        if (ScanParam.scan == Status.START):
            if (stan == 0):
                ImCont.dir = 0
                ImCont.x = ImCont.x + 1
                PictureData.CH1[ImCont.y, ImCont.x] = np.mean(SampleMode.f_ch1[int(marg):int(maks-marg)])
                PictureData.CH2[ImCont.y, ImCont.x] = np.mean(SampleMode.f_ch2[int(marg):int(maks-marg)]) 
                if (ImCont.x == (resolution - 1)):
                    stan = 1
                
            elif (stan == 1):
                ImCont.x = ImCont.x
                stan = 2
                # if (parametrImCont.y['tImCont.ype'] == 'snake'):
                # ImCont.y = ImCont.y + 1

            elif (stan == 2):
                ImCont.dir = 1
                PictureData.CH3[ImCont.y, ImCont.x] = np.mean(np.mean(SampleMode.f_ch1[int(marg):int(maks-marg)]))
                PictureData.CH4[ImCont.y, ImCont.x] = np.mean(SampleMode.f_ch2[int(marg):int(maks-marg)]) 
                ImCont.x = ImCont.x - 1
                if (ImCont.x == 0):
                    stan = 3
                    
            elif (stan == 3):                 
                ImCont.x = ImCont.x
                ImCont.y = ImCont.y + 1
                ImCont.oY = ImCont.oY + 1
                PictureData.line = PictureData.line + 1
                if(ImCont.oY == resolution):
                    FileOperations.save_manager_files()
                    ImCont.oY = 0
                    ScanParam.scan = Status.STOP
                stan = 0
                # print(PictureData.line, old_PictureData.line)
                # Tutaj dodac kalkulacje srredniej dla X,Y dla kazdego kanału i zamiana 0 na srednia z poprzedniej linii pomiarowej

        else:
            ImCont.dir = 0
            stan = 0
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
        

# animation function.  This is called sequentially
def update_pictures(i):
    resolution = ScanParam.resolution

    ax1.cla()
    ax1.set_title("CH 1 - TOPO L->P")
    ax2.cla()
    ax2.set_title("CH 2 - ERROR L->P")
    ax5.cla()
    ax5.set_title("CH 1 - TOPO P->L")
    ax6.cla()
    ax6.set_title("CH 2 - ERROR P->L")

    ax1.imshow(PictureData.CH1,  cmap='Oranges_r', interpolation='none') 
    ax2.imshow(PictureData.CH2,  cmap='afmhot', interpolation='none')
    ax5.imshow(PictureData.CH3,  cmap='Oranges_r', interpolation='none') 
    ax6.imshow(PictureData.CH4,  cmap='afmhot', interpolation='none')
    
    x = np.linspace(0, SampleMode.sample, SampleMode.sample)
    ox = np.linspace(1,resolution,resolution)
   
    if(i % 2 == 1):
        ax3.clear()
        ax3.set_ylabel("CH 1 - TOPO", color="C1")
        ax3.tick_params(axis='x', colors="C1")
        ax3.tick_params(axis='y', colors="C1")
        if(ScanParam.scan == Status.STOP):
            ax3.plot(x, SampleMode.DataCH1, color="C1")
        else:
            if(ImCont.dir == 0):
                if(ImCont.oY == 0):
                    ax3.plot(ox[1:resolution], PictureData.CH1[ImCont.oY,1:resolution], color="C1")
                else:
                    ax3.plot(ox[1:resolution], PictureData.CH1[ImCont.oY,1:resolution], ox[1:resolution], PictureData.CH1[(ImCont.oY-1),1:resolution], color="C1")
            else:
                if(ImCont.oY == 0):
                    ax3.plot(ox[1:resolution], PictureData.CH3[ImCont.oY,1:resolution], color="C1")
                else:
                    ax3.plot(ox[1:resolution], PictureData.CH3[ImCont.oY,1:resolution], ox[1:resolution], PictureData.CH3[(ImCont.oY-1),1:resolution], color="C1")
    else:
        ax4.clear()
        ax4.yaxis.tick_right()
        ax4.set_xlabel('Samples', color="C0")
        ax4.set_ylabel('CH 2 - ERROR', color="C0")       
        ax4.yaxis.set_label_position('right') 
        ax4.tick_params(axis='x', colors="C0")
        ax4.tick_params(axis='y', colors="C0")
        if(ScanParam.scan == Status.STOP):
            # ax4.plot(x, SampleMode.DataCH2, color="C0")
            line1.set_ydata(SampleMode.DataCH2)
            # fig.canvas.draw()
        else:
            if(ImCont.dir == 0):
                if(ImCont.oY == 0):
                    ax4.plot(ox[1:resolution], PictureData.CH2[ImCont.oY,1:resolution], color="C0")
                else:
                    ax4.plot(ox[1:resolution], PictureData.CH2[ImCont.oY,1:resolution], ox[1:resolution], PictureData.CH2[(ImCont.oY-1),1:resolution], color="C0")
            else:
                if(ImCont.oY == 0):
                    ax4.plot(ox[1:resolution], PictureData.CH4[ImCont.oY,1:resolution], color="C0")
                else:
                    ax4.plot(ox[1:resolution], PictureData.CH4[ImCont.oY,1:resolution], ox[1:resolution], PictureData.CH4[(ImCont.oY-1),1:resolution], color="C0")
   

def commands_and_menu():
    while(ScanParam.scan != Status.EXIT):
        MenuControll.run()
        if(PictureData.save == Status.YES):
            FileOperations.save_manager_files()
            PictureData.save = Status.NO
        time.sleep(0.2)
    plt.close()


def on_close(event):
    FileOperations.save_manager_files()
    MenuControll.show_menu_parameters()
    end_threads()
    quit()


def end_threads():
    ScanParam.scan = Status.EXIT
    print("Locking all dragons in dungeons o-]===> ")
    time.sleep(2)
    if(t1.is_alive()):
        t1.join()
        t1.terminate()
    if(t2.is_alive()):
        t2.join()
        t2.terminate()


if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')

    Device.Check_device()
    Device.Open_device()
    MenuControll.menu_header()

    t1 = threading.Thread(target=commands_and_menu, args=())
    t2 = threading.Thread(target= Start_AD2, args=())
  
    t1.start()
    t2.start()

    fig.canvas.mpl_connect('close_event', on_close)
    ani = animation.FuncAnimation(fig, update_pictures, frames=50, interval=20)
    
    plt.show()
    
    # plt.close()
    # on_close()
    end_threads()
    MenuControll.menu_end()
    quit()