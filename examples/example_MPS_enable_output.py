import pyB12MPS
import time

mps = pyB12MPS.MPS() # Initialize MPS class

mps.power(0) # Set Power to 0 dBm
mps.freq(9.5) # Set Frequency to 9.5 GHz
mps.wgstatus(1) # Enable WG Switch for DNP Mode
mps.rfstatus(1) # Enable RF Output

time.sleep(3) # Delay 3 seconds

mps.rfstatus(0) # Disable RF Output
mps.wgstatus(0) # Disable WG Switch (back to EPR mode)

mps.close() # Close the Connection to MPS
