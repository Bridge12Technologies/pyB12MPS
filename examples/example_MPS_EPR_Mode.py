import pyB12MPS
import time

freq = 9.52832 # GHz
lo_power = 10 # dBm
power = 15 # dBm

mps = pyB12MPS.MPS() # initialize MPS class

time.sleep(0.1)
mps.freq(freq) # Set Frequency
time.sleep(0.1)
mps.power(power) # Set Power
time.sleep(0.1)
mps.send_command('lofreq %i'%(freq*1e6)) # Set LO Frequency
time.sleep(0.1)
mps.send_command('lopower %i'%(lo_power*10)) # Set LO Power
time.sleep(0.1)
mps.send_command('loenable 1') # Set LO Enable
time.sleep(0.1)
mps.send_command('lophase 0') # Set LO Phase
time.sleep(0.1)
mps.wgstatus(1) # Enable WG switch
time.sleep(0.1)
mps.rfstatus(1) # Enable RF Output






# if port cannot be found automatically specify the port manually:
# mps.pyB12MPS.MPS(port = 'COM3')

#mps.freq(9.75) # set frequency to 9.75 GHz

#mps.power(5) # set power to 5 dBm

#mps.close() # close connection to MPS

#del mps # delete class
