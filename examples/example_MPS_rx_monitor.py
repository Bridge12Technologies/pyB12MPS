import pyB12MPS

mps = pyB12MPS.MPS() # initialize MPS class


pts = 1000 # Set Number of points

for ix in range(pts):
    rx_voltage = mps.rxpowermv() # read Rx voltage in mV
    print(ix, rx_voltage, 'mV') # print result


mps.close() # close MPS connection
