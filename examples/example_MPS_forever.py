import pyB12MPS

mps = pyB12MPS.MPS()

ix = 0
while True:
    rx = mps.rxpowermv()
    print(ix, rx, 'mV')
    ix += 1
