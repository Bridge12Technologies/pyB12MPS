import pyB12MPS
import time

mps = pyB12MPS.MPS() # initialize MPS class


pts = 100 # Set Number of points

for ix in range(pts):
    time.sleep(1)
    rx_power_dBm = mps.rxpowerdbm() # read Rx voltage in dBm
    print('Reading:', ix)
    print('Rx Power:', rx_power_dBm, 'dBm') # print result
    rx_power_mv = mps.rxpowermv() # read Rx voltage in mv
    print('Rx Voltage:', rx_power_mv, 'mv') # print result
    tx_power_dBm = mps.txpowerdbm() # read Rx voltage in dBm
    print('Tx Power:', tx_power_dBm, 'dBm') # print result
    tx_power_mv = mps.txpowermv() # read Rx voltage in mV
    print('Tx Voltage:', tx_power_mv, 'mV') # print result
    print('-'*30)


mps.close() # close MPS connection
