# README #

pyB12MPS is a python package for interfacing with Bridge12 MPS.

The complete online documentation for the Bridge12 MPS is available [here](http://mps.bridge12.com).

The complete online documentation for pyB12MPS is available [here](http://pyb12mps.bridge12.com).


### Requirements ###

* Python3 (>= 3.6)
* numpy, pySerial

```console
python -m pip install numpy
python -m pip install pyserial
```

### Communicating with the Bridge12 MPS ###

First make sure the Bridge12 MPS is connected to the computer via a USB cable and the system is powered ON.

In a terminal window, start a python environment

```console
python
```

To start the MPS Server:

```python
import pyB12MPS as mps

mps.start()
```

The MPS will reset and the python environment will hang until the connection has been established. The server will run in the background until the stop command is sent.

To stop the MPS Server:

```
mps.stop()
```

### Sending Client Commands ###

Once the connection has been established, you can use the client script to send commands to the MPS.

```python
import pyB12MPS as mps

mps.freq(9.4) # set frequency to 9.4 GHz

mps.freq() # Query the microwave frequency in GHz
```

### Example Script ###

```python
import pyB12MPS as mps
import time

# Start Bridge12 MPS server
mps.start()

# number of points to acquire
pts = 10

# Delay time between measurements
dt = 1.

# Pre-allocate list for storing voltages
rxVoltageList = []

for ix in range(pts):
    # delay in seconds
    time.sleep(dt)

    # read Rx voltage in mV
    rxVoltage = mps.rxpowermv()

    # Append Rx voltage to list
    rxVoltageList.append(rxVoltage)

# Display the result
print(rxVoltageList)

# Stop Bridge12 MPS Server
mps.stop()
```
