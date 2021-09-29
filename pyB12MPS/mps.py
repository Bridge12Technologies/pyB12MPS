import numpy as np
import serial
import time
import os
import sys
import serial.tools.list_ports


class MPS:
    def __init__(self, port = None):
        if port == None:
            self.port = self.detectMPSSerialPort()

        self.init()

    def init(self):
        print('Connecting to MPS using port %s'%self.port)
        self.ser = serial.Serial(self.port, 115200, timeout = 1.)
        time.sleep(3)
        from_mps_string = ''
#        while self.ser.in_waiting:
        while from_mps_string != 'System Ready':
            from_mps_bytes = self.ser.readline()
            from_mps_string = from_mps_bytes.decode('utf-8').rstrip()
            print(from_mps_string)

        # Catch "Synthesizer detected"
        time.sleep(1)
        self.flush()

    def ampgain(self, gain = None):
        '''Advanced feature to adjust gain for calibration of MPS

        Args:
            gain (None, float, int): Amplifier gain in dBm

        Returns:
            float: if gain is None, returns the current amplifier gain value in dBm
        '''

        if gain is not None:
            gain = gain * 10
            gainString = str(int(gain))
            self.send_command('ampgain %s'%gainString)

        else:
            gainString = self.send_command('ampgain?', recv = True)
            gain = float(gainString) / 10.

            return gain

    def ampstatus(self, ampState = None):
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
            self.send_command('ampstatus %s'%ampStateString)
        else:
            ampStateString = self.send_command('ampstatus?',recv = True)
            ampState = int(ampStateString)
            return ampState

    def amptemp(self):
        ''' Query the MPS amplifier temperature

        Returns:
            ampTemp (float): Amplifier temperature in degrees C
        '''

        ampTempString = self.send_command('amptemp?',recv = True)
        ampTemp = float(ampTempString) / 10.
        return ampTemp


    def close(self):
        '''Close serial port
        '''
        self.ser.close()

    def debug(self, debugMode = None):
        '''Query/Set debug mode of MPS

        Args:
            debugMode (None, int): If None, query the debug mode. Otherwise set the debug mode.

        Returns:
            debugMode (int): If query, returns current debug mode of MPS
        '''

        if debugMode is not None:
            if debugMode in (0,1):
                self.send_command('debug %i'%debugMode)
            else:
                raise ValueError('Debug mode must be 0 or 1')
        else:
            debugModeString = self.send_command('debug?', recv = True)
            debugMode = int(debugModeString)
            return debugMode

    def detectMPSSerialPort(self):
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

    def firmware(self):
        '''Query the MPS firmware version

        Returns:
            firmwareVersion (str): Firmware version
        '''
        firmwareVersion = self.send_command('firmware?',recv = True)
        return firmwareVersion

    def flush(self):
        '''Flush the MPS Serial Buffer
        '''
        self.ser.reset_input_buffer() # reset and flush buffer

    def freq(self, freqValue = None):
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
            
            self.send_command('freq %s'%str_freq)

        else: # Query the frequency
            return_kHz_freq = self.send_command('freq?',recv = True)
            return_freq = float(return_kHz_freq) / 1.e6 # convert to GHz
            return return_freq

    def id(self):
        '''Query the instrument identificationstring of MPS

        Returns:
            idString (str): ID of instrument: "Bridge12 MPS"
        '''
        idString = self.send_command('id?',recv = True)
        return idString

    def in_waiting(self):
        '''Return bytes in MPS serial port

        Returns:
            value (int): number of bytes at serial port
        '''

        return self.ser.in_waiting

    def listPorts(self):
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

    def lockstatus(self, lockState = None):
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
                self.send_command('lockstatus %i'%lockState)
            else:
                raise ValueError('Lock State Not Valid')
        else:
            lockStateString = self.send_command('lockstatus?', recv = True)
            lockState = int(lockStateString)
            return lockState


    def lockdelay(self, delay = None):
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
                    self.send_command('lockdelay %i'%delay)
                else:
                    raise ValueError('Lock delay must be greater than %i and less than %i ms'%(minDelay,maxDelay))
            else:
                raise ValueError('Lock delay must be int or float')
        else:
            lockReadingString = self.send_command('lockdelay?',recv = True)
            lockReading = int(lockReadingString)
            return lockReading

    def lockstep(self, step = None):
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
                    self.send_command('lockstep %i'%step)
                else:
                    raise ValueError('Frequency step must be greater than %i minStep and less than %i maxStep kHz'%(minStep,maxStep))
            else:
                raise ValueError('Frequency step must be float or integer')
        else:
            stepReadingString = self.send_command('lockstep?',recv = True)
            stepReading = int(stepReadingString)

            return stepReading

    def power(self, powerValue = None):
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
            
            self.send_command('power %s'%str_power)

        else: # Query the power
            return_tenth_dB_power = self.send_command('power?',recv = True)
            return_power = float(return_tenth_dB_power) / 10. # convert to dBm
            return return_power

    def rfstatus(self, rfState = None):
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
                self.send_command('rfstatus %i'%rfState)
            else:
                raise ValueError('RF Status Not Valid')
        else:
            rfStateReadingString = self.send_command('rfstatus?',recv = True)
            rfStateReading = int(rfStateReadingString)
            return rfStateReading

    def rfsweepdata(self):
        '''Get data from RF sweep

        Returns:
            numpy.array: Tuning curve from previous rf sweep

        Example::

            data = mps.rfsweepdata()

        '''

        returnDataRfSweep = self.send_command('rfsweepdata?',recv = True)
        returnDataRfSweep = returnDataRfSweep.rstrip()
        returnDataRfSweep = np.fromstring(returnDataRfSweep,sep=',')
        returnValues = returnDataRfSweep.astype(int)

        return returnValues

    def rfsweepdosweep(self):
        '''Start single RF Sweep.

        Example::

            mps.rfsweepdosweep()

        '''

        self.send_command('rfsweepdosweep?')

    def rfsweeppower(self, tunePower = None):
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
            self.send_command('rfsweeppower %s'%tunePowerString)
        else:
            tunePowerString = self.send_command('rfsweeppower?', recv = True)
            tunePower = float(tunePowerString) / 10.

            return tunePower

    def rfsweepnpts(self, rfSweepNptsValue = None):
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
            self.send_command('rfsweepnpts %s'%rfSweepNptsValue)
        else: # Query
            returnRfSweepNpts = self.send_command('rfsweepnpts?',recv = True)
            returnRfSweepNpts = int(returnRfSweepNpts)
            return returnRfSweepNpts

    def rfsweepdwelltime(self, dwellTime = None):
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
            dwellTimeString = self.send_command('rfsweepdwelltime?', recv = True)
            dwellTime = float(dwellTimeString)

            return dwellTime

    def rfsweepinitialdwelltime(self, dwellTime = None):
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
            self.send_command('rfsweepinitialdwelltime %s'%dwellTimeString)
        else:
            dwellTimeString = self.send_command('rfsweepinitialdwelltime?', recv = True)
            dwellTime = float(dwellTimeString)

            return dwellTime

    def rfsweepsw(self, rfSweepSwValue = None):
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
            self.send_command('rfsweepsw %s'%rfSweepSwValue)
        else: # Query
            returnRfSweepSw = self.send_command('rfsweepsw?',recv = True)
            returnRfSweepSw = int(returnRfSweepSw)
            return returnRfSweepSw

    def rxdiodesn(self):
        '''Query serial number of Rx diode

        Returns:
            serialNumberRx (str): Serial number string of Rx diode
        '''
        serialNumberRx = self.send_command('rxdiodesn?',recv = True)
        return serialNumberRx

    def rxpowerdbm(self):
        '''Query the Rx diode reading in dBm

        Returns:
            rxPower (float): Reciever monitor power reading in dBm

        Example::

            rxPower = rxpowerdbm() # Query Rx diode power reading

        '''
        return_tenth_rx_dbm = self.send_command('rxpowerdbm?',recv = True)
        rxPower = float(return_tenth_rx_dbm) / 10. # convert to dBm
        return rxPower

    def rxpowermv(self):
        '''Query the Rx diode reading in mV

        Returns:
            rxVoltage (float): Receiver monitor voltage reading in mV

        Example::

            rxVoltage = rxpowermv() # Query Rx diode voltage

        '''
        return_tenth_rx_mv = self.send_command('rxpowermv?',recv = True)
        rxVoltage = float(return_tenth_rx_mv) / 10. # convert to mV
        return rxVoltage

    def screen(self, screenState = None):
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
                self.send_command('screen %i'%screenState)
            else:
                raise ValueError('Screen Status is not Valid')
        else:
            screenStateReadingString = self.send_command('screen?',recv = True)
            screenStateReading = int(screenStateReadingString)
            return screenStateReading

    def send_command(self, command, recv = False):
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

        self.ser.reset_input_buffer() # reset and flush buffer

        send_string = '%s\n'%command

        # specify string as utf-8
        send_bytes = send_string.encode('utf-8')

        # send bytes to MPS
        self.ser.write(send_bytes)

        # read bytes from MPS
        from_mps_bytes = self.ser.readline()
        from_mps_string = from_mps_bytes.decode('utf-8').rstrip()

        return from_mps_string

    def serialNumber(self):
        '''Query serial number of MPS

        Returns:
            serialNumber (str): Serial number string of MPS
        '''
        serialNumberString = self.send_command('serial?',recv = True)
        return serialNumberString

    def systemstatus(self):
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
        systemStatusString = self.send_command('systemstatus?',recv = True)

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
        systemStatusDict['screen'] = int(systemStatusDict['screen'])

        return systemStatusDict

    def trig(self):
        '''Output Trigger pulse from MPS

        Example::

            trig()

        '''
        self.send_command('trig')

    def triglength(self, length = None):
        '''Set/Query trigger pulse length in us

        Args:
            length (None, float, int): If given, the length of the trigger pulse in us. If None, queries the trigger pulse length.

        Returns:
            (int) trigger pulse length in us.

        Example::

            triglength(100) # Set trigger pulse length to 100 us
            triglength() # query the trigger pulse length

        '''
        if length is None:
            length = self.send_command('triglength?', recv = True)
            length = int(length)
            return length
        else:
            if (length > 0) and (length <= 10000000):
                self.send_command('triglength %i'%length)
            else:
                raise ValueError('Trigger Length must be less than or equal to 10 seconds.')

    def txdiodesn(self):
        '''Query serial number of Tx diode
        
        Returns:
            serialNumberTx (str): Serial number string of Tx diode
        '''
        serialNumberTx = self.send_command('txdiodesn?',recv = True)
        return serialNumberTx

    def txpowerdbm(self):
        ''' Returns transmitter power monitor in dBm

        Returns:
            txPower (float): Transmitter power monitor voltage in dBm

        Example::

            txPower = txpowerdbm() # Query Tx diode power reading

        '''
        return_tenth_tx_dbm = self.send_command('txpowerdbm?',recv = True)
        txPower = float(return_tenth_tx_dbm) / 10. # convert to dBm
        return txPower

    def txpowermv(self):
        ''' Returns transmitter power monitor in mV

        Returns:
            txVoltage (float): Transmitter power monitor voltage in mV

        Example::

            txVoltage = txpowermv() # Query Tx diode voltage

        '''
        return_tenth_tx_mv = self.send_command('txpowermv?',recv = True)
        txVoltage = float(return_tenth_tx_mv) / 10. # convert to mV
        return txVoltage

    def wgstatus(self, wgStatus = None):
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
                self.send_command('wgstatus %i'%wgStatus)
            else:
                raise ValueError('WG Status Not Valid')
        else:
            wgStatusReadingString = self.send_command('wgstatus?',recv = True)
            wgStatusReading = int(wgStatusReadingString)
            return wgStatusReading

if __name__ == '__main__':
    pass
