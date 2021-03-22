=================
Quick-Start Guide
=================

--------
Overview
--------

The pyB12MPS python package consists of a python server module
:doc:`pyB12MPS Server <pyB12MPS-Server>`
and a python client module
:doc:`pyB12MPS Module <pyB12MPS>`.

The python server establishes a socket connection to the MPS. The server must be running in the background for the client module to send commands to the Bridge12 MPS. Instructions for a user to remote control the Bridge12 MPS from a terminal window are summarized in section :ref:`Sec_Communicating_with_MPS`.

For the more experienced user and to help debugging user-written applications the server and client module can be started in two different instances. This approach is described in section :ref:`Debugging`.


.. note::
    Make sure the Bridge12 MPS is connected to the computer. To connect the Bridge12 MPS to a computer a USB-A to USB-A cable is required.


.. _Sec_Communicating_with_MPS:

-----------------------------------
Communicating with the Bridge12 MPS
-----------------------------------

In a terminal window start a python environment

.. code-block:: console

    python

Now you can import the pyB12MPS module and start the server in the background

.. code-block:: python

    import pyB12MPS as mps

    mps.start()

The pyB12MPS module will open a socket to the Bridge12 MPS in the background. The unit will reset and after initialization return to the main screen. Once the main screen is displayed, the Bridge12 MPS is ready to receive commands from the terminal. In most terminal applications you have to hit the return key once to get back to the prompt.

There are two types of commands that you can send to the Bridge12 MPS, queries and set commands. In general, queries will have no argumnets, while a set command requires an argument. For example to query the frequency

.. code-block:: python

    mps.freq()
    9.553

The system will return the current microwave frequency in GHz. In this case 9.553 GHz.

To set the frequency send this command

.. code-block:: python

    mps.freq(9.673)

This will set the microwave frequency to 9.673 GHz. A complete list of client commands can be found :doc:`here <pyB12MPS>`.

To close the connection to the Bridge12 MPS send this command

.. code-block:: python

    mps.stop()
    Communication with MPS stopped

This will stop the serial communication with the system and close the serial socket server, which is running in the background.

.. warning::
    When using pyB12MPS on Mac or Linux, do not just close the terminal window to terminate the program. This will not stop the server in the background and you will not be able to start the server successfully again.
    If the window is closed accidentally, you need to manually kill the python process that runs the socket server.

    On Mac/Linux: In a terminal window type:
    
        .. code-block:: console

            ps
        
    to get a list of the active processes. Identify the python process and use the kill command with the PID to kill the corresponding process.

    On Windows: The python process can be terminated by opening the Task Manager, selecting the python process and clicking the "End task" button.

---------
Debugging
---------

Starting the Server
-------------------

In a terminal start the server by running:

.. code-block:: console
    
    python pyB12MPS_server.py

Make sure you are in the same directory as the pyB12MPS_server.py file. In this directory, you will also find a serverConfig.py file. The serverConfig.py file contains the IP and PORT information for the server as well as other initialization information. If the "autoDetectSerialPort" variable in the serverConfig.py file is set to True, the script will automatically detect the serial port the MPS is connected to and start the python server.

Alternatively, you can specify the serial port by giving this as an argument. In this case, the automatic detection of the serial port will be overridden. For example to specify com port 3 (COM3):

.. code-block:: console
    
    python pyB12MPS_server.py COM3

Once the connection has been established, you can use the client script to send commands to the MPS.

Sending Client Commands
-----------------------

A complete list of client commands can be found :doc:`here <pyB12MPS>`.

To set the frequency to 9.4 GHz:

.. code-block:: python

    import pyB12MPS as mps

    mps.freq(9.4)

To set the microwave power to 10 dBm:

.. code-block:: python

    import pyB12MPS as mps

    mps.power(10)

Example - Reading Diode Voltage
-------------------------------

.. code-block:: python

    import pyB12MPS as mps
    import time

    # Number of points to acquire
    pts = 10

    # Time delay between readings in seconds
    dt = 1.

    # pre-allocate list of Rx voltage readings
    rxVoltageList = []

    for ix in range(pts):
        # Delay before reading
        time.sleep(dt)

        # Read Rx voltage in mV
        rxVoltage = mps.rxpowermv()

        # Print the Rx voltage reading
        print('Rx Voltage: %0.01f'%rxVoltage)

        # Append data to list
        rxVoltageList.append(rxVoltage)

    # Print Result
    print('Rx Voltage Readings:')
    print(rxVoltageList)

