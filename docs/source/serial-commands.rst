===============
Serial Commands
===============

Serial Port Settings
--------------------

+--------------+----------------------------------+
|Parameter     |Value                             |
+==============+==================================+
|Baud Rate     |115200                            |
+--------------+----------------------------------+
|Data Bits     |8                                 |
+--------------+----------------------------------+
|Parity Bit    |No                                |
+--------------+----------------------------------+
|Stop Bit      |1                                 |
+--------------+----------------------------------+

Command Syntax
--------------

The syntax for setting a parameter through the serial interface is the command followed by the value. The command and value are separated by a space (" ").

**"freq 9540000<CR>"**

Query commands are followed by a question mark ("?"). The general structure to query a parameter is:

**"freq?<CR>"**

List of Serial Commands
-----------------------

+--------------+-------------------------------------------+
|Command       |Description                                |
+==============+===========================================+
|help          |Get help instructions                      |
+--------------+-------------------------------------------+
|freq          |Set/query microwave frequency in kHz       |
+--------------+-------------------------------------------+
|power         |Set/query microwave power in dBm times 10  |
+--------------+-------------------------------------------+
|rxpowermv     |Query Rx diode reading in mV times 10      |
+--------------+-------------------------------------------+
|rxpowerdbm    |Query Rx diode power in dBm times 10       |
+--------------+-------------------------------------------+
|txpowermv     |Query Tx diode reading in mV times 10      |
+--------------+-------------------------------------------+
|txpowerdbm    |Query Tx diode power in dBm times 10       |
+--------------+-------------------------------------------+
|rfstatus      |Set/Query RF status                        |
+--------------+-------------------------------------------+
|wgstatus      |Set/Query Waveguide status                 |
+--------------+-------------------------------------------+
|ampstatus     |Set/Query amplifier power                  |
+--------------+-------------------------------------------+
|amptemp       |Query amplifier temperature                |
+--------------+-------------------------------------------+
|lockstatus    |Set/Query frequency lock                   |
+--------------+-------------------------------------------+
|lockdelay     |Set/Query frequency lock delay in ms       |
+--------------+-------------------------------------------+
|lockstep      |Set/Query frequency lock step in kHz       |
+--------------+-------------------------------------------+
|screen        |Set/Query Display Screen                   |
+--------------+-------------------------------------------+
|firmware      |Query firmware version                     |
+--------------+-------------------------------------------+
|id            |Query MPS ID                               |
+--------------+-------------------------------------------+
|serial        |Query serial number                        |
+--------------+-------------------------------------------+
|rxdiodessn    |Query Rx diode serial number               |
+--------------+-------------------------------------------+
|txdiodessn    |Query Tx diode serial number               |
+--------------+-------------------------------------------+
|debug         |Set debug mode on/off                      |
+--------------+-------------------------------------------+

Example with pySerial
---------------------

::
    
    import serial
    import time

    # MPS Serial Port
    serialPort = 'COM5'

    # Start Serial Connection
    ser = serial.Serial(serialPort,115200,timeout = 1.)
    time.sleep(0.1)

    system_ready_string = 'Synthesizer detected'

    # Initialize MPS
    while not is_system_ready:
        time.sleep(0.1)
        bytes_in_waiting = ser.in_waiting
        if bytes_in_waiting > 0:
            read_bytes = ser.readline()
            read_string = read_bytes.decode('utf-8').rstrip()
            print(read_string)
            if read_string == system_ready_string:
                is_system_ready = True

    # Command to send to MPS
    command = 'freq 9400000\n'

    # Encode MPS command (convert to bytes)
    command_bytes = command.encode('utf-8')

    # Send command to MPS
    ser.write(command_bytes)
