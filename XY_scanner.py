import sys
import matplotlib
import threading
import time
import numpy as np
import os

from ctypes import *
from dwfconstants import *
from matplotlib import pyplot as plt
from matplotlib import animation

from src.scan_data import ImCont, PictureData, ScanSample, DwfData, ScanParam

np.random.seed(19680801)
CONST_MENU_REPEAT = 10
#declare ctype variables
hdwf = c_int()
sts = c_byte()

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'
width, height = os.get_terminal_size()

par = { 'oxy' : 3.0, 'dx' : 0.0, 'dy' : 0.0, 
        'adc1' : 't', 'adc2' : 't', 'dac1' : 'n', 'dac2' : 'n',
        'int' : 'n', 'scan' : 'n', 'save' : 'n',
        'log' : 'n', 
        'exit' : 't'}

com = ['sample', 'freq']


if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")


# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
gs = fig.add_gridspec(2,4)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax5 = fig.add_subplot(gs[0, 2])
ax6 = fig.add_subplot(gs[0, 3])
ax3 = fig.add_subplot(gs[1, :], label="1")
ax4 = fig.add_subplot(gs[1, :], label="2", frame_on=False)


def cykacz():
    global PictureData
    global ImCont
    global ScanSample
    stan = 0

    resolution = ScanParam.resolution

    while (par['exit'] == 't'):
        
        dxy = 2 * par['oxy'] / resolution
        
        d1 = (ImCont.x * dxy) + par['dx'] - (par['oxy'])
        d2 = (ImCont.y * dxy) + par['dy'] - (par['oxy'])
        
        dwf.FDwfAnalogOutNodeOffsetSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(d1))
        dwf.FDwfAnalogOutNodeOffsetSet(hdwf, c_int(1), AnalogOutNodeCarrier, c_double(d2))
        
        start_osciloscope()

        if(DwfData.hzAcq[0] != DwfData.hzAcq[1]):
            DwfData.hzAcq[1] = DwfData.hzAcq[0]
            dwf.FDwfAnalogInFrequencySet(hdwf, DwfData.hzAcq[0])
            dwf.FDwfAnalogInRecordLengthSet(hdwf, c_double((ScanSample.sample/DwfData.hzAcq[0].value) - 1))
            DwfData.logError = "Data frequency success updated in device"

        for i in range(ScanSample.sample):
            ScanSample.f_ch1[i] = float(ScanSample.DataCH1[i])
            ScanSample.f_ch2[i] = float(ScanSample.DataCH2[i])
        
        maks = ScanSample.sample
        marg = 0.1 * maks
        
        if(par['exit'] == 'n'):
            break

        # PictureData.CH2[y, ImCont.x] = np.mean(ScanSample.f_ch2) 

        if (par['scan'] == 't'):
            if (stan == 0):
                ImCont.dir = 0
                ImCont.x = ImCont.x + 1
                PictureData.CH1[ImCont.y, ImCont.x] = np.mean(ScanSample.f_ch1[int(marg):int(maks-marg)])
                PictureData.CH2[ImCont.y, ImCont.x] = np.mean(ScanSample.f_ch2[int(marg):int(maks-marg)]) 
                if (ImCont.x == (resolution - 1)):
                    stan = 1
                
            elif (stan == 1):
                ImCont.x = ImCont.x
                stan = 2
                # if (parametrImCont.y['tImCont.ype'] == 'snake'):
                # ImCont.y = ImCont.y + 1

            elif (stan == 2):
                ImCont.dir = 1
                PictureData.CH3[ImCont.y, ImCont.x] = np.mean(np.mean(ScanSample.f_ch1[int(marg):int(maks-marg)]))
                PictureData.CH4[ImCont.y, ImCont.x] = np.mean(ScanSample.f_ch2[int(marg):int(maks-marg)]) 
                ImCont.x = ImCont.x - 1
                if (ImCont.x == 0):
                    stan = 3
                    
            elif (stan == 3):                 
                ImCont.x = ImCont.x
                ImCont.y = ImCont.y + 1
                ImCont.oY = ImCont.oY + 1
                PictureData.line = PictureData.line + 1
                if(ImCont.oY == resolution):
                    save_files()
                    ImCont.oY = 0
                    par['scan'] = 'n'
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
        
        if ((PictureData.line > 0) and (PictureData.line < resolution) and (par['int'] == 't') ):
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

        
#print(DWF version
def check_device():
    version = create_string_buffer(16)
    dwf.FDwfGetVersion(version)
    DwfData.version = " " + str(version.value)
    print(DwfData.version)


#open device
def open_device():
    DwfData.status = "Opening first device"
    dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

    if hdwf.value == hdwfNone.value:
        szerr = create_string_buffer(512)
        dwf.FDwfGetLastErrorMsg(szerr)
        print(str(szerr.value))
        DwfData.status = "Failed to open device :("
    else:
        #set up acquisition 
        dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_bool(True))
        dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(1), c_bool(True))
        dwf.FDwfAnalogInAcquisitionModeSet(hdwf, acqmodeRecord)
        # dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(ScanSample.sample))
        dwf.FDwfAnalogInFrequencySet(hdwf, DwfData.hzAcq[0])
        dwf.FDwfAnalogInRecordLengthSet(hdwf, c_double((ScanSample.sample/DwfData.hzAcq[0].value) - 1)) 

        dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_bool(True))
        dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), AnalogOutNodeCarrier, funcDC)
        dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(1), AnalogOutNodeCarrier, c_bool(True))
        dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(1), AnalogOutNodeCarrier, funcDC)
        #wait at least 2 seconds for the offset to stabilize
        time.sleep(2)

def start_osciloscope():
    global ImCont
    global par
    csamples = 0

    dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))

    while csamples < ScanSample.sample:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
        if csamples == 0 and (sts == DwfStateConfig or sts == DwfStatePrefill or sts == DwfStateArmed) :
            continue # Acquisition not yet started.

        dwf.FDwfAnalogInStatusRecord(hdwf, byref(DwfData.cAvailable), byref(DwfData.cLost), byref(DwfData.cCorrupted))
        
        csamples += DwfData.cLost.value

        if DwfData.cLost.value :
            DwfData.fLost = 1
        if DwfData.cCorrupted.value :
            DwfData.fCorrupted = 1

        if DwfData.cAvailable.value==0 :
            continue

        if csamples+DwfData.cAvailable.value > ScanSample.sample :
            DwfData.cAvailable = c_int(ScanSample.sample-csamples)
        
        dwf.FDwfAnalogInStatusData(hdwf, c_int(0), byref(ScanSample.DataCH1, sizeof(c_double)*csamples), DwfData.cAvailable) # get channel 1 data
        dwf.FDwfAnalogInStatusData(hdwf, c_int(1), byref(ScanSample.DataCH2, sizeof(c_double)*csamples), DwfData.cAvailable) # get channel 2 data
        csamples += DwfData.cAvailable.value
        
        if(par['exit'] == 'n'):
            break

    if (par['log'] == 't'):
        local_time = "[" + time.strftime("%H:%M:%S",time.localtime()) + "] "
        if DwfData.fLost:
            DwfData.logError = local_time + "Samples were lost! Reduce frequency"
            par['log'] = 'n'
        if DwfData.fCorrupted:
            DwfData.logError = local_time + "Samples could be corrupted! Reduce frequency"
            par['log'] = 'n'


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

    ax1.imshow(PictureData.CH1,  cmap='Oranges', interpolation='none') 
    ax2.imshow(PictureData.CH2,  cmap='afmhot', interpolation='none')
    ax5.imshow(PictureData.CH3,  cmap='Oranges', interpolation='none') 
    ax6.imshow(PictureData.CH4,  cmap='afmhot', interpolation='none')
    
    x = np.linspace(0, ScanSample.sample, ScanSample.sample)
    ox = np.linspace(1,resolution,resolution)
   
    if(i % 2 == 1):
        if (par['adc1'] == 't'): 
            ax3.clear()
            ax3.set_ylabel("CH 1 - TOPO", color="C1")
            ax3.tick_params(axis='x', colors="C1")
            ax3.tick_params(axis='y', colors="C1")
            if(par['scan'] == 'n'):
                ax3.plot(x, ScanSample.DataCH1, color="C1")
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
        if (par['adc2'] == 't'):
            ax4.clear()
            ax4.yaxis.tick_right()
            ax4.set_xlabel('Samples', color="C0")
            ax4.set_ylabel('CH 2 - ERROR', color="C0")       
            ax4.yaxis.set_label_position('right') 
            ax4.tick_params(axis='x', colors="C0")
            ax4.tick_params(axis='y', colors="C0")
            if(par['scan'] == 'n'):
                ax4.plot(x, ScanSample.DataCH2, color="C0")
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
   

def update_values_in_datas(command, value):
    global par
    global ImCont
    global ScanSample
    try:
        par[command] = float(value)
    except  ValueError:
        par[command] = value
    
    if(command == 'sample' ):
        dana = int(value) % 20000
        ScanSample.sample = dana
        ScanSample.DataCH1 = (c_double*ScanSample.sample)()
        ScanSample.DataCH2= (c_double*ScanSample.sample)()
        ScanSample.f_ch1 = np.arange(ScanSample.sample, dtype=float)
        ScanSample.f_ch2 = np.arange(ScanSample.sample, dtype=float)
    
    if(command == 'freq' ):
        dana = (int(value) % 2000) * 1000
        DwfData.hzAcq[0] = c_double(dana)


def menu_header():
    txt = "XY Scanner - STM / AFM"
    header = txt.center(width)
    print("="*width)
    print(header,)
    print("="*width)
    

def menu_parameters():
    print ("")
    print("Status: \t", ScanParam.resolution, "     ")
    print("Resolution: \t", ScanParam.resolution, "     ")
    print("Scan sample: \t", ScanSample.sample, "     ")
    print("Scan freq: \t", DwfData.hzAcq[0].value, "     ")
    print("="*width)
    print("DWF Ver: \t" + DwfData.version, "     ")
    print("Log: \t\t", DwfData.logError, "     ")
    print("-"*width)


def menu_param_revrite(revrite):
    for i in range (revrite):
            print(LINE_UP, end='\r')


def menu_end():
    print("-"*width)
    txt = "Exit program - Come back soon! :-) "
    goodby_txt = txt.center(width)
    print(goodby_txt)
    print("-"*width)


def obsluga_komend():
    global par
    while(par['exit'] == 't'):

        menu_parameters()
        print(" " * width, end='\r')
        wej = input("Get param: \t ")
        menu_param_revrite(CONST_MENU_REPEAT)
            
        lista = wej.split()
        if((lista[0].lower() in par) or (lista[0].lower() in com) ):
            update_values_in_datas(lista[0].lower(), lista[1])
            txt = "Value updated"
            DwfData.logError = txt + (" " * 5)
        else:
            DwfData.logError = "Incorrectly entered command!"
        
        if(par['save'] == 't'):
            par['save'] = 'n'
            save_files()
        time.sleep(1)
        
    plt.close()


def save_files():
    named_tuple = time.localtime()
    time_string = time.strftime("%Y-%m-%d_%H-%M-%S", named_tuple)
    np.savetxt( 'data\CH1_T'+ time_string +'.txt', PictureData.CH1, fmt="%10.5f", delimiter=";")
    np.savetxt( 'data\CH1_E'+ time_string +'.txt', PictureData.CH2, fmt="%10.5f", delimiter=";")
    np.savetxt( 'data\CH2_T'+ time_string +'.txt', PictureData.CH3, fmt="%10.5f", delimiter=";")
    np.savetxt( 'data\CH2_E'+ time_string +'.txt', PictureData.CH4, fmt="%10.5f", delimiter=";")
    matplotlib.image.imsave('data\CH1_T'+ time_string + '.png', PictureData.CH1)
    matplotlib.image.imsave('data\CH1_E'+ time_string + '.png', PictureData.CH2)
    matplotlib.image.imsave('data\CH2_T'+ time_string + '.png', PictureData.CH3)
    matplotlib.image.imsave('data\CH2_E'+ time_string + '.png', PictureData.CH4)
    # print('ALL files saved: ' + time_string + ' ]:-> ')
    DwfData.logError = 'ALL files saved: ' + time_string + ' ]:-> '


def on_close(event):
    save_files()
    menu_parameters()
    end_threads()
    quit()


def end_threads():
    global par
    par['exit'] = 'n'
    print("Zamykanie")
    # time.sleep(2)
    if(t1.is_alive()):
        print("Zamykanie watku t1")
        t1.join()
        # t1.terminate()
    if(t2.is_alive()):
        print("Zamykanie watku t2")
        t2.join()
        # t2.terminate()


if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')

    check_device()
    open_device()
    menu_header()

    t1 = threading.Thread(target=obsluga_komend, args=())
    t2 = threading.Thread(target=cykacz, args=())
  
    t1.start()
    t2.start()

    fig.canvas.mpl_connect('close_event', on_close)
    ani = animation.FuncAnimation(fig, update_pictures, frames=50, interval=20)
    
    plt.show()
    
    # plt.close()
    # on_close()
    end_threads()
    menu_end()
    quit()