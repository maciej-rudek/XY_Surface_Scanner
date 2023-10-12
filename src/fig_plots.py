import numpy as np
from matplotlib import pyplot as plt

class pic():
    fig = plt.figure()
    gs = fig.add_gridspec(2,4)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax5 = fig.add_subplot(gs[0, 2])
    ax6 = fig.add_subplot(gs[0, 3])
    axA = fig.add_subplot(gs[0, 0:2])
    axB = fig.add_subplot(gs[0, 2:4])
    axC = fig.add_subplot(gs[0, 0:4])
    ax3 = fig.add_subplot(gs[1, :], label="1")
    ax4 = fig.add_subplot(gs[1, :], label="2", frame_on=False)
    x = np.linspace(0, 10*np.pi, 100)
    y = np.sin(x)
    line1, = ax4.plot(x, y, 'b-')
    
    
    def pic_visable(status):
        pic.gs.set_visible(status)
       
        
    def ax_all_visable_off():
        pic.ax_1256_visable(False)
        pic.ax_AB_visable(False)
        pic.ax_C_visable(False)
        

    def ax_1256_visable(status):
        pic.ax1.set_visible(status)
        pic.ax2.set_visible(status)
        pic.ax5.set_visible(status)
        pic.ax6.set_visible(status)
    
    
    def ax_AB_visable(status):
        pic.axA.set_visible(status)
        pic.axB.set_visible(status)
    
    
    def ax_C_visable(status):
        pic.axC.set_visible(status)