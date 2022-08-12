# README #

pyB12MPS is a python package for interfacing with Bridge12 MPS.

The complete online documentation for the Bridge12 MPS is available [here](http://mps.bridge12.com).

The complete online documentation for pyB12MPS is available [here](http://pyb12mps.bridge12.com).


### Requirements ###

* Python3 (>= 3.6)
* numpy, pySerial

### Communicating with the Bridge12 MPS ###

First make sure the Bridge12 MPS is connected to the computer via a USB cable and the system is powered ON.

In a terminal window, start a python environment

```console
python
```

```python
import pyB12MPS

mps = pyB12MPS.MPS()
```

The MPS will reset and the python environment will hang until the MPS has initialized.

To close the MPS serial port:

```
mps.close()
```

### Sending MPS Commands ###

Once the connection has been established, you can send commands to the MPS.

```python

mps.freq(9.4) # set frequency to 9.4 GHz

mps.freq() # Query the microwave frequency in GHz
```

### Example Script ###

```python
import pyB12MPS
import time

mps = pyB12MPS.MPS()

# Number of Rx voltage points to acquire
pts = 10

# Time delay between measurements in seconds
dt = 0.5

rxVoltageList = []

for ix in range(pts):
    # delay
    time.sleep(dt)

    # Read MPS Rx diode voltage
    rxVoltage = mps.rxpowermv()

    # Print Rx voltage reading
    print('Rx Voltage: %0.01f'%rxVoltage)

    rxVoltageList.append(rxVoltage)

print('Rx Voltage Readings:')
print(rxVoltageList)
```
