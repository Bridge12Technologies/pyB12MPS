import pyB12MPS

mps = pyB12MPS.MPS()

mps.power(0)
mps.freq(9.5)
mps.wgstatus(1)
mps.rfstatus(1)
mps.close()
