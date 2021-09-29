import pyB12MPS
import time

mps = pyB12MPS.MPS()

mps.power(0)
mps.freq(9.5)
mps.wgstatus(1)
mps.rfstatus(1)

time.sleep(3)

mps.rfstatus(0)
mps.wgstatus(0)

mps.close()
