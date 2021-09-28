import pyB12MPS

mps = pyB12MPS.MPS() # initialize MPS class

# if port cannot be found automatically specify the port manually:
# mps.pyB12MPS.MPS(port = 'COM3')

mps.freq(9.75) # set frequency to 9.75 GHz

mps.power(5) # set power to 5 dBm

mps.close() # close connection to MPS
