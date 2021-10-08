import pyB12MPS as mps
from pylab import *
mps.start()
print(f"power {mps.rfsweeppower()}",
    f"points {mps.rfsweepnpts()}",
    f"dw {mps.rfsweepdwelltime()}",
    f"freq {mps.freq()}",
    f"initial dwell {mps.rfsweepinitialdwelltime()}",
    f"SW {mps.rfsweepsw()}")
typical_range = r_[9.819,9.825]
mps.freq(typical_range.mean().item())
mps.rfsweepsw(3)
print(f"before first run:\n\tpower {mps.rfsweeppower()}",
    f"points {mps.rfsweepnpts()}",
    f"dw {mps.rfsweepdwelltime()}",
    f"freq {mps.freq()}",
    f"initial dwell {mps.rfsweepinitialdwelltime()}",
    f"SW {mps.rfsweepsw()}")
#mps.rfsweepdosweep()
for j in range(20):
    data = mps.rfsweepdata()
    print(data)
#mps.freq(typical_range.mean().item()+0.005)
#print(f"before second run:\n\tpower {mps.rfsweeppower()}",
#    f"points {mps.rfsweepnpts()}",
#    f"dw {mps.rfsweepdwelltime()}",
#    f"freq {mps.freq()}",
#    f"initial dwell {mps.rfsweepinitialdwelltime()}",
#    f"SW {mps.rfsweepsw()}")
#mps.rfsweepdosweep()
#data2 = mps.rfsweepdata()
plot(data)
mps.stop()
show()

