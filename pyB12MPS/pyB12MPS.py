import numpy as np
import socket
import time
import os
import subprocess
import sys
from . import serverConfig
import serial.tools.list_ports

HOST = serverConfig.HOST
PORT = serverConfig.PORT

initializeOnStart = serverConfig.initializeOnStart
defaultSerialPort = serverConfig.defaultSerialPort
serialDelay = serverConfig.serialDelay

autoDetectSerialPort = serverConfig.autoDetectSerialPort
systemReadyString = serverConfig.systemReadyString


path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

def ampgain(gain = None):
    '''Advanced feature to adjust gain for calibration of MPS

    Args:
        gain (None, float, int): Amplifier gain in dBm

    Returns:
        float: if gain is None, returns the current amplifier gain value in dBm
    '''

    if gain is not None:
        gain = gain * 10
        gainString = str(int(gain))
        send_command('ampgain %s'%gainString)

    else:
        gainString = send_command('ampgain?', recv = True)
        gain = float(gainString) / 10.

        return gain

def ampstatus(ampState = None):
    ''' Query MPS microwave amplifier status

    +---------+----------------------+
    |ampState |Description           |
    +=========+======================+
    |0        |Amplifier Off         |
    +---------+----------------------+
    |1        |Amplifier On          |
    +---------+----------------------+
    |2        |Amplifier Ext         |
    +---------+----------------------+

    Returns:
        ampState (int): Amplifier status of MPS
    '''

    if ampState is not None:
        if ampState not in (0,1,2):
            raise ValueError('Invalid Amplifier State. Must be 0, 1, 2')
        ampState = int(ampState)

        ampStateString = str(ampState)
        send_command('ampstatus %s'%ampStateString)
    else:
        ampStateString = send_command('ampstatus?',recv = True)
        ampState = int(ampStateString)
        return ampState

def amptemp():
    ''' Query the MPS amplifier temperature

    Returns:
        ampTemp (float): Amplifier temperature in degrees C
    '''

    ampTempString = send_command('amptemp?',recv = True)
    ampTemp = float(ampTempString) / 10.
    return ampTemp


def close():
    '''Close serial port
    '''
    send_command('_close_')

    print('Closing serial socket...')

    isMPSReady = systemReady()
    if (isMPSReady == 0):
        print('Serial socket closed')
    else:
        print('Failed to close serial socket')

def debug(debugMode = None):
    '''Query/Set debug mode of MPS

    Args:
        debugMode (None, int): If None, query the debug mode. Otherwise set the debug mode.

    Returns:
        debugMode (int): If query, returns current debug mode of MPS
    '''

    if debugMode is not None:
        if debugMode in (0,1):
            send_command('debug %i'%debugMode)
        else:
            raise ValueError('Debug mode must be 0 or 1')
    else:
        debugModeString = send_command('debug?', recv = True)
        debugMode = int(debugModeString)
        return debugMode

def detectMPSSerialPort():
    '''Return the serial port for the MPS

    Returns:
        str: MPS serial port. If MPS serial port is not found, uses the default serial port.
    '''

    print('Automatically Detecting Serial Port...')
    ports = list(serial.tools.list_ports.comports())
    MPSDetected = False
    for p in ports:
        print(p)
        if (p.vid == 9025 or p.vid == 10755):
            MPSDetected = True
            MPSPort = p.device
            print('MPS Detected on port %s'%(MPSPort))
    if MPSDetected:
        serialPort = MPSPort
    else:
        print('Automatic detection failed.')
        serialPort = None
    return serialPort

def firmware():
    '''Query the MPS firmware version

    Returns:
        firmwareVersion (str): Firmware version
    '''
    firmwareVersion = send_command('firmware?',recv = True)
    return firmwareVersion

def flush():
    '''Flush the MPS Serial Buffer
    '''
    send_command('_flush_')

def freq(freqValue = None):
    ''' Set/Query Microwave Frequency

    Args:
        freqValue (int, float): Set Frequency in GHz, by default this parameter is None and the frequency is queried

    Returns:
        frequency in GHz

    Example::

        microwaveFrequency = freq() # Query Microwave Frequency

        freq(9.4) # Set Microwave Frequency to 9.4 GHz

    '''
    max_freq = 100.
    if freqValue is not None:
        if not isinstance(freqValue,(float,int)):
            raise ValueError('Frequency value must be an float or int')
        if (freqValue > max_freq):
            raise ValueError('Frequency value must be in units of GHz')
        freqValue = float(freqValue)
        kHz_freq = freqValue * 1.e6
        str_freq = '%0.0f'%kHz_freq
        
        send_command('freq %s'%str_freq)

    else: # Query the frequency
        return_kHz_freq = send_command('freq?',recv = True)
        return_freq = float(return_kHz_freq) / 1.e6 # convert to GHz
        return return_freq

def id():
    '''Query the instrument identificationstring of MPS

    Returns:
        idString (str): ID of instrument: "Bridge12 MPS"
    '''
    idString = send_command('id?',recv = True)
    return idString

def in_waiting():
    '''Return bytes in MPS serial port

    Returns:
        value (int): number of bytes at serial port
    '''
    value_string = send_command('_in_waiting_',recv = True)
    value = int(value_string)
    return value

def listPorts():
    '''List the serial ports available. This function is for troubleshooting when the serial port of the MPS is unknown.

    Returns:
        portsAvailable (dict): Dictionary of Serial Ports. Key is serial port. Value is description.

    Example::

        portsAvailable = listPorts() # Return Dictionary of Serial Ports Available
    '''

    portsAvailable = {}
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print('*'*50)
        print('serial port: ' + str(p.device))
        print('description: ' + str(p.description))
        portsAvailable[p.device] = p.description
    print('*'*50)
    return portsAvailable

def lockstatus(lockState = None,verifyOperateMode = True):
    '''Set/Query the frequency lock, must be performed in operate mode

    +---------+----------------------+
    |lockState|Description           |
    +=========+======================+
    |0        |Disable Frequency Lock|
    +---------+----------------------+
    |1        |Enable Frequency Lock |
    +---------+----------------------+

    Args:
        lockState (None, int): if lockState is not None, sets the lock state
        verifyOperateMode (bool): If True, verifies that the operate mode is enabled before setting the lock state

    Warning:
        The frequency lock can only be enabled in operate mode (screen() returns 1).

    Returns:
        lockState (int): Frequency lock state of MPS

    Example::

        lockState = lockstatus() # Query the Frequency Lock Status

        lockstatus(0) # Diable Frequency Lock
        lockstatus(1) # Enable Frequency Lock

    '''
    if lockState is not None:
        if lockState in (0,1):
            if verifyOperateMode:
                #Check for operate mode with 
                screenState = screen()
                if screenState != 2:
                    raise ValueError('Screen State Must be Operate Mode for Lock Mode')
                rfState = rfstatus()
                if rfState != 1:
                    raise ValueError('RF Output Must be enabled for lock Mode')
            send_command('lockstatus %i'%lockState)

        else:
            raise ValueError('Lock State Not Valid')
    else:
        lockStateString = send_command('lockstatus?', recv = True)
        lockState = int(lockStateString)
        return lockState


def lockdelay(delay = None):
    '''Set/Query lock delay in ms

    Args:
        delay (None, int, float): Frequency lock delay in ms

    Returns:
        delayReading (int): If delay is None, returns lock delay value

    Example::

        delay = lockdelay() # Query the Frequency Lock Delay in ms

        lockdelay(100) # Set the Frequency Lock Delay to 100 ms

    '''
    minDelay = 100.
    maxDelay = 500.

    if delay is not None:
        if isinstance(delay,(int,float)):
            if (delay >= minDelay) and (delay <= maxDelay):
                delay = int(delay)
                send_command('lockdelay %i'%delay)
            else:
                raise ValueError('Lock delay must be greater than %i and less than %i ms'%(minDelay,maxDelay))
        else:
            raise ValueError('Lock delay must be int or float')
    else:
        lockReadingString = send_command('lockdelay?',recv = True)
        lockReading = int(lockReadingString)
        return lockReading

def lockstep(step = None):
    '''Set/Query Lock frequency step in kHz

    Args:
        step (None, int, float): Frequency lock step in kHz

    Returns:
        stepReading (int): If step is None, returns current lock step value in kHz

    Example::

        step = lockstep() # Query the Lock Frequency Step in kHz

        lockstep(20) # Set the Frequency Lock Step to 20 kHz

    '''
    minStep = 10.
    maxStep = 50.
    if step is not None:
        if isinstance(step,(int,float)):
            if (step >= minStep) and (step <= maxStep):
                step = int(step)
                send_command('lockstep %i'%step)
            else:
                raise ValueError('Frequency step must be greater than %i minStep and less than %i maxStep kHz'%(minStep,maxStep))
        else:
            raise ValueError('Frequency step must be float or integer')
    else:
        stepReadingString = send_command('lockstep?',recv = True)
        stepReading = int(stepReadingString)

        return stepReading

def open():
    '''Initialize MPS serial port connection
    '''
    send_command('_init_')

    isMPSReady = systemReady()

    if (isMPSReady == 1):
        print('System Ready')
    else:
        print('System failed to start')

def power(powerValue = None):
    '''Set/Query Microwave Power

    Args:
        powerValue (None, int, float): Set Power in dBm, by default this parameter is None and the power is queried

    Returns:
        powerValue (float): Microwave power in dBm 

    Example::

        powerValue = power() # Query Microwave Power

        power(10) # Set microwave power to 10 dBm

    '''
    if powerValue is not None:
        if not isinstance(powerValue,(float,int)):
            raise ValueError('Power value must be an float or int')
        powerValue = float(powerValue)
        tenth_dB_power = powerValue * 10.
        str_power = '%0.0f'%tenth_dB_power
        
        send_command('power %s'%str_power)

    else: # Query the power
        return_tenth_dB_power = send_command('power?',recv = True)
        return_power = float(return_tenth_dB_power) / 10. # convert to dBm
        return return_power

def rfstatus(rfState = None,verifyWaveguideStatus = True):
    ''' Set/Query the RF status

    +-------+---------------------------------+
    |rfState|Description                      |
    +=======+=================================+
    |0      |Disable RF Output                |
    +-------+---------------------------------+
    |1      |Enable RF Output                 |
    +-------+---------------------------------+
    |2      |External Trigger Microwave Output|
    +-------+---------------------------------+
    
    Args:
        rfState (None, int): RF Status value
        verifyWaveguideStatus (bool): Check if waveguide status is Enabled (True by default).

    Returns:
        rfStateReading (int): If rfStatus is not None, returns queried RF status

    Warning:
        The microwave output (rfstatus(1)) can only be enabled if the waveguide switch is set to DNP mode (wgstatus() returns 1).
        

    Example::

        rfState = rfstatus() # Query the RF State

        rfstatus(0) # Disable Microwave Output
        rfstatus(1) # Enable Microwave Output
        rfstatus(2) # Enable External Trigger of Microwave Output

    '''
    if rfState is not None:
        if rfState in (0,1,2):
            if verifyWaveguideStatus:
                waveguideState = wgstatus()
                if waveguideState == 1:
                    send_command('rfstatus %i'%rfState)
                else:
                    raise ValueError('Waveguide Switch is Disabled (EPR Mode)')
            else:
                send_command('rfstatus %i'%rfState)
        else:
            raise ValueError('RF Status Not Valid')
    else:
        rfStateReadingString = send_command('rfstatus?',recv = True)
        rfStateReading = int(rfStateReadingString)
        return rfStateReading

def rfsweepdata():
    '''Get data from RF sweep

    Returns:
        numpy.array: Tuning curve from previous rf sweep

    Example::

        data = mps.rfsweepdata()

    '''

    returnDataRfSweep = send_command('rfsweepdata?',recv = True)
    returnDataRfSweep = returnDataRfSweep.rstrip()
    returnDataRfSweep = np.fromstring(returnDataRfSweep,sep=',')
    returnValues = returnDataRfSweep.astype(int)

    return returnValues

def rfsweepdosweep():
    '''Start single RF Sweep.

    Example::

        mps.rfsweepdosweep()

    '''

    send_command('rfsweepdosweep?')

def rfsweeppower(tunePower = None):
    '''Set/Query Power for RF Sweep

    Args:
        tunePower (None, float, int): If not None, sets the rf sweep power to this value in dBm. Otherwise queries the current rf sweep power.

    Returns:
        float: If tunePower argument is None, the current rf sweep power.

    Example::
        
        mps.rfsweeppower(15) # set rf sweep power to 15 dBm
        tunePower = mps.rfsweepPower()

    '''

    if tunePower is not None:
        if not isinstance(tunePower,(int,float)):
            raise ValueError('Value must be an int or float')
        tunePower = tunePower * 10
        tunePowerString = str(int(tunePower))
        send_command('rfsweeppower %s'%tunePowerString)
    else:
        tunePowerString = send_command('rfsweeppower?', recv = True)
        tunePower = float(tunePowerString) / 10.

        return tunePower

def rfsweepnpts(rfSweepNptsValue = None):
    ''' Set/query number of points in RF sweep

    Args:
        rfsweepnpts(int): Set number of points in RF sweep. If empty, number of points is queried

    Returns:
        int: If rfSweepNptsValue argument is None, the number of point in the rf sweep

    Example::
        
        pts = rfsweepnpts() # query the number of points in rf sweep
        rfsweepnpts(100) # set the number of points in rf sweep to 100

    '''
    if rfSweepNptsValue is not None:
        if not isinstance(rfSweepNptsValue,int):
            raise ValueError('Value must be an int')
        send_command('rfsweepnpts %s'%rfSweepNptsValue)
    else: # Query
        returnRfSweepNpts = send_command('rfsweepnpts?',recv = True)
        returnRfSweepNpts = int(returnRfSweepNpts)
        return returnRfSweepNpts

def rfsweepdwelltime(dwellTime = None):
    '''Rf sweep dwell time in us

    Args:
        dwellTime: If dwellTime is not None, value to set the RF sweep dwell time in us

    Returns:
        float: If dwellTime is None, the current value of the rf sweep dwell time in us.

    Example::

        rfsweepdwelltime(50) # set rf sweep dwell time to 50 us
        dwellTime = rfsweepdwelltime() # Query the rf sweep dwell time

    '''

    if dwellTime is not None:
        if not isinstance(dwellTime,(int,float)):
            raise ValueError('Value must be an int')
        dwellTimeString = str(dwellTime)
        send_command('rfsweepdwelltime %s'%dwellTimeString)
    else:
        dwellTimeString = send_command('rfsweepdwelltime?', recv = True)
        dwellTime = float(dwellTimeString)

        return dwellTime

def rfsweepinitialdwelltime(dwellTime = None):
    '''Rf sweep dwell time in ms for first point

    Args:
        dwellTime: If dwellTime is not None, value to set the RF sweep dwell time for the first point in ms

    Returns:
        float: If dwellTime is None, the current value of the RF sweep dwell time for the first point in ms.

    Example::

        mps.rfsweepinitialdwelltime(100) # Set the dwell time for the first point to 100 ms
        dwellTime = mps.rfsweepinitialdwelltime() # Query the dwell time for the first point in ms

    '''

    if dwellTime is not None:
        if not isinstance(dwellTime,(int,float)):
            raise ValueError('Value must be an int')
        dwellTimeString = str(dwellTime)
        send_command('rfsweepinitialdwelltime %s'%dwellTimeString)
    else:
        dwellTimeString = send_command('rfsweepinitialdwelltime?', recv = True)
        dwellTime = float(dwellTimeString)

        return dwellTime

def rfsweepsw(rfSweepSwValue = None):
    ''' Set/query predefined RF sweep width (MHs)

    +-----------+----------------------------+
    | rfsweepsw | Value                      |
    +===========+============================+
    | 0         | 250 MHz                    |
    +-----------+----------------------------+
    | 1         | 100 MHz                    |
    +-----------+----------------------------+
    | 2         | 50 MHz                     |
    +-----------+----------------------------+
    | 3         | 10 MHz                     |
    +-----------+----------------------------+

    Args:
        rfsweepsw(int): rfsweepsw variable which determines the rf sweep width. If None, number of points is queried

    Returns:
        int: rf sweep width

    Example::

        mps.rfsweepsw(0) # set rf sweep width to 250 MHz
        sweepWidth = mps.rfsweepsw() # Query current rf sweep width

    '''

    if rfSweepSwValue is not None:
        if not isinstance(rfSweepSwValue,int):
            raise ValueError('Value must be an int')
        send_command('rfsweepsw %s'%rfSweepSwValue)
    else: # Query
        returnRfSweepSw = send_command('rfsweepsw?',recv = True)
        returnRfSweepSw = int(returnRfSweepSw)
        return returnRfSweepSw

def rxdiodesn():
    '''Query serial number of Rx diode

    Returns:
        serialNumberRx (str): Serial number string of Rx diode
    '''
    serialNumberRx = send_command('rxdiodesn?',recv = True)
    return serialNumberRx

def rxpowerdbm():
    '''Query the Rx diode reading in dBm

    Returns:
        rxPower (float): Reciever monitor power reading in dBm

    Example::

        rxPower = rxpowerdbm() # Query Rx diode power reading

    '''
    return_tenth_rx_dbm = send_command('rxpowerdbm?',recv = True)
    rxPower = float(return_tenth_rx_dbm) / 10. # convert to dBm
    return rxPower

def rxpowermv():
    '''Query the Rx diode reading in mV

    Returns:
        rxVoltage (float): Receiver monitor voltage reading in mV

    Example::

        rxVoltage = rxpowermv() # Query Rx diode voltage

    '''
    return_tenth_rx_mv = send_command('rxpowermv?',recv = True)
    rxVoltage = float(return_tenth_rx_mv) / 10. # convert to mV
    return rxVoltage

def screen(screenState = None):
    '''Set/Query Screen Status

    +--------------+----------------+
    | screen       | Description    |
    +==============+================+
    | 0            | Main Screen    |
    +--------------+----------------+
    | 1            | Operate Screen |
    +--------------+----------------+
    | 2            | Sweep Screen   |
    +--------------+----------------+
    | 3            | Advanced Screen|
    +--------------+----------------+

    Args:
        screenState (None, int): If screenState is not None, sets the screen state

    Returns:
        screenStateReading (int): If screenState is None, returns the screen state

    Example::

        screenState = screen() # Query the Screen Status

        screenstatus(0) # Set Screen to Main Screen
        screenstatus(1) # Set Screen to Operate Screen
        screenstatus(2) # Set Screen to Sweep Screen
        screenstatus(3) # Set Screen to Advanced Screen

    '''

    if screenState is not None:
        if screenState in (0,1,2):
            send_command('screen %i'%screenState)
        else:
            raise ValueError('Screen Status is not Valid')
    else:
        screenStateReadingString = send_command('screen?',recv = True)
        screenStateReading = int(screenStateReadingString)
        return screenStateReading

def send_command(command, recv = False):
    '''Send string command to python MPS server

    Args:
        command (str): string command to be sent to MPS Server
        recv (bool): True if serial port should be read after writing. False by default.

    Returns:
        recv_string (str): if recv = True, returns string received from MPS Server

    Example::

        send_command('freq 9300000') # Set Frequency to 9.3 GHz

        freqStringkHz = send_command('freq?',recv = True) # Query the microwave frequency in kHz
        freqValue = float(freqStringkHz) / 1.e6 # Convert frequency string float in units of GHz

        send_command('_stop_') # Stop the python server

    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST,PORT))

    send_string = '%s\n'%command

    # specify string as utf-8
    send_bytes = send_string.encode('utf-8')

    # send bytes to server
    s.sendall(send_bytes)

    # serial delay
    time.sleep(serialDelay)

    if recv:
        recv_bytes = s.recv(1024)
        recv_string = recv_bytes.decode('utf-8')
        recv_string = recv_string.rstrip()

        s.close()

        return recv_string
    else:
        s.close()

def serialNumber():
    '''Query serial number of MPS

    Returns:
        serialNumber (str): Serial number string of MPS
    '''
    serialNumberString = send_command('serial?',recv = True)
    return serialNumberString

def set_host(host):
    global HOST
    HOST = host

def set_port(port):
    global PORT
    PORT = port

def start(serialPort = None, host = None, port = None, debug = False):

    '''Start python TCP server

    Args:
        serialPort (None, str): If given, serial port to establish MPS connection.
        ip (None, str): If given, the IP address to use for the server
        port (None, str); If given, the port to use for the server

    Example::

        start() # Start python server with automatically detected serial port or default serial port (defined in configuration file)

        start('COM5') # Start python server using "COM5" as serial port
    '''
    # Need HOST and PORT to be global
    global HOST
    global PORT

    args = []
    if serialPort is not None:
        args += [serialPort]
    elif autoDetectSerialPort:
        serialPort =  detectMPSSerialPort()
        if serialPort == None:
            print('\nCannot automatically connect to MPS.\nPlease specify COM Port manually.')
            return
        args += [serialPort]

    if host is None:
        host = HOST
    args += [host]

    if port is None:
        port = PORT
    args += [str(port)]
    
    HOST = host
    PORT = port
    print()
    print('--- Server Parameters ---')
    print('Serial Port: %s'%serialPort)
    print('HOST: %s'%host)
    print('PORT: %s'%port)
    print('-------------------------')
    print()

    if debug == True:
        print('Starting Subprocess')
        p = subprocess.Popen([sys.executable, '-m', 'pyB12MPS'] + args, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.STDOUT,
                                    shell = True,
                                    creationflags = subprocess.DETACHED_PROCESS)
    else:
        p = subprocess.Popen([sys.executable, '-m', 'pyB12MPS'] + args, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.STDOUT)
    
    print('Server starting...')

    serverErrorIndicator = test()
    errorCounter = 0

    while (serverErrorIndicator != 0):
        
        time.sleep(0.1)
        serverErrorIndicator = test()
        print('Server Error Code: %s'%serverErrorIndicator)
        errorCounter += 1

        if (p.poll() is not None) or (errorCounter >= 50):
            print()
            print('Server failed to start.')
            print()
            print('Please visit the Troubleshooting section of the ')
            print('online documentation at pyB12MPS.bridge12.com for')
            print('more information.')
            print()
            return

    if serverErrorIndicator == 0:
        print('Server started.')

    print('MPS initializing...')

    ### Check for MPS Initialization ###
    if initializeOnStart:
        open()

def stop():
    '''Stop python server 
    '''
    send_command('_stop_')

    serverErrorIndicator = test()
    errorCounter = 0

    while (serverErrorIndicator == 0):
        time.sleep(0.1)
        serverErrorIndicator = test()
        errorCounter += 1

        if (errorCounter >= 50):
            print('Failed to stop server.')
            break

    if serverErrorIndicator != 0:
        print('Server stopped.')

def systemReady():
    '''Query python server for initialized status of MPS

    +-----------+--------------------------------------+
    |isMPSReady |Description                           |
    +===========+======================================+
    |0          |MPS Serial Connection Not Initialized |
    +-----------+--------------------------------------+
    |1          |MPS Serial Connection Initialized     |
    +-----------+--------------------------------------+
    
    Returns:
        isMPSReady (int): RF Status value
    '''
    isMPSReady = send_command('_is_system_ready_',recv = True)
    isMPSReady = int(isMPSReady.rstrip())
    return isMPSReady

def systemstatus():
    '''Returns dictionary of MPS status

    +--------------------------------------+
    |Keys                                  |
    +======================================+
    |freq                                  |
    +--------------------------------------+
    |power                                 |
    +--------------------------------------+
    |rxpowermv                             |
    +--------------------------------------+
    |txpowermv                             |
    +--------------------------------------+
    |rfstatus                              |
    +--------------------------------------+
    |wgstatus                              |
    +--------------------------------------+
    |ampstatus                             |
    +--------------------------------------+
    |amptemp                               |
    +--------------------------------------+
    |lockstatus                            |
    +--------------------------------------+
    |screen                                |
    +--------------------------------------+


    Returns:
        dict: dictionary of system status variables
    '''
    systemStatusString = send_command('systemstatus?',recv = True)

    systemStatusList = systemStatusString.rstrip().split(',')

    systemStatusDict = {}

    for statusInfo in systemStatusList:
        key, value = tuple(statusInfo.split(':'))

        systemStatusDict[key] = value

    systemStatusDict['freq'] = float(systemStatusDict['freq']) / 1.e6
    systemStatusDict['power'] = float(systemStatusDict['power']) / 10.
    systemStatusDict['rxpowermv'] = float(systemStatusDict['rxpowermv']) / 10.
    systemStatusDict['txpowermv'] = float(systemStatusDict['txpowermv']) / 10.
    systemStatusDict['rfstatus'] = int(systemStatusDict['rfstatus'])
    systemStatusDict['wgstatus'] = int(systemStatusDict['wgstatus'])
    systemStatusDict['ampstatus'] = int(systemStatusDict['ampstatus'])
    systemStatusDict['amptemp'] = float(systemStatusDict['amptemp']) / 10.
    systemStatusDict['lockstatus'] = int(systemStatusDict['lockstatus'])
    systemStatusDict['screen'] = int(systemStatusDict['screen'])

    return systemStatusDict

def test():
    '''Test Server Connection

    Returns:
        serverErrorIndicator: A value of zero (0) indicates normal operation of the server. Any other value indicates a server error.
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverErrorIndicator = s.connect_ex((HOST,PORT))
    s.close()
    return serverErrorIndicator

def trig():
    '''Instructs MPS to send Trigger pulse
    '''
    send_command('trig')

def triglength(length = None):
    '''Set trigger length in us
    '''
    if length is None:
        length = send_command('triglength?', recv = True)
        length = int(length)
        return length
    else:
        if (length > 0) and (length <= 10000000):
            send_command('triglength %i'%length)
        else:
            raise ValueError('Trigger Length must be less than or equal to 10 seconds.')

def txdiodesn():
    '''Query serial number of Tx diode
    
    Returns:
        serialNumberTx (str): Serial number string of Tx diode
    '''
    serialNumberTx = send_command('txdiodesn?',recv = True)
    return serialNumberTx

def txpowerdbm():
    ''' Returns transmitter power monitor in dBm

    Returns:
        txPower (float): Transmitter power monitor voltage in dBm

    Example::

        txPower = txpowerdbm() # Query Tx diode power reading

    '''
    return_tenth_tx_dbm = send_command('txpowerdbm?',recv = True)
    txPower = float(return_tenth_tx_dbm) / 10. # convert to dBm
    return txPower

def txpowermv():
    ''' Returns transmitter power monitor in mV

    Returns:
        txVoltage (float): Transmitter power monitor voltage in mV

    Example::

        txVoltage = txpowermv() # Query Tx diode voltage

    '''
    return_tenth_tx_mv = send_command('txpowermv?',recv = True)
    txVoltage = float(return_tenth_tx_mv) / 10. # convert to mV
    return txVoltage

def wgstatus(wgStatus = None):
    ''' Set/Query the waveguide switch (wg) status

    +--------+-----------------------------------+
    |wgStatus|Description                        |
    +========+===================================+
    |0       |Disable Waveguide Switch (EPR Mode)|
    +--------+-----------------------------------+
    |1       |Enable Waveguide Switch (DNP Mode) |
    +--------+-----------------------------------+

    Args:
        wgStatus (None, int): wg status value

    Returns:
        wgStatusReading (int): If wgStatus is not None, returns queried wg status

    Example::

        wgState = wgstatus() # Query the Waveguide State

        wgstatus(0) # Switch to EPR Mode
        wgstatus(1) # Switch to DNP Mode

    '''
    if wgStatus is not None:
        if wgStatus in (0,1):
            send_command('wgstatus %i'%wgStatus)
        else:
            raise ValueError('WG Status Not Valid')
    else:
        wgStatusReadingString = send_command('wgstatus?',recv = True)
        wgStatusReading = int(wgStatusReadingString)
        return wgStatusReading

if __name__ == '__main__':
    pass
