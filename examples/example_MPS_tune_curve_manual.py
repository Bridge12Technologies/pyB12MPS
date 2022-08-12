import pyB12MPS
import numpy as np
import matplotlib.pylab as plt
import time

# Parameters
start_freq = 9.4 # GHz
stop_freq = 9.6 # GHz
points = 100
power_level = 0 # dBm

f = np.linspace(start_freq, stop_freq, points)

mps = pyB12MPS.MPS() # initialize class

mps.freq(f[0]) # set MPS to initial frequency
mps.power(power_level) # set MPS power level for sweep
mps.wgstatus(1) # Enable WG status
mps.rfstatus(1) # Enable RF output

Rx_list = [] # create list of Rx diode values

# Sweep Frequency and record Rx monitor values
for freq_ix, freq in enumerate(f):
    mps.freq(freq) # Set frequency
    time.sleep(0.05) # delay for rx diode reading
    Rx = mps.rxpowermv() # Read Rx diode voltage
    print('%i of %i'%(freq_ix,points),'%0.05f GHz :'%freq, Rx, 'mV') # Print Result
    Rx_list.append(Rx) # append Rx value to list

Rx_array = np.array(Rx_list) # Convert python list to numpy array

mps.rfstatus(0)
mps.wgstatus(1)

mps.close() # close serial connection
del mps # delete class

plt.figure()
plt.plot(f, Rx_array, color = '#F37021')
plt.grid(linestyle = ':', color = '#4D4D4F')
plt.xlabel('Frequency (GHz)')
plt.ylabel('Rx Diode Voltage (mV)')
plt.show()

