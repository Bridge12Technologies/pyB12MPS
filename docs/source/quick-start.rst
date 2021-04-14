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

If you experience any issues with the package please see the :ref:`troubleshooting` section.


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


Sending Client Commands
-----------------------

Here we briefly go over a few useful commands. A complete list of MPS commands can be found :doc:`here <pyB12MPS>`.

To set the frequency to 9.4 GHz:

.. code-block:: python

    mps.freq(9.4)

To set the microwave power to 10 dBm:

.. code-block:: python

    mps.power(10)

To turn the WG switch to DNP mode:

.. code-block:: python

    mps.wgstatus(1)

To turn on the RF output:

.. code-block:: python

    mps.rfstatus(1)

The Rx and Tx diode voltages in mV can be queried as follows:

.. code-block:: python

    mps.rxpowermv()
    mps.txpowermv()

The RF output off and WG switch back to EPR mode:

.. code-block:: python

    mps.wgstatus(0)

Example Script - Reading Diode Voltage
--------------------------------------

.. code-block:: python

    import pyB12MPS as mps
    import time

    # Test if server is running
    if mps.test(): # 0 indicates normal operation of server
        mps.start(debug = True)

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

        # Append voltage reading to list
        rxVoltageList.append(rxVoltage)

    # print result
    print('Rx Voltage Readings:')
    print(rxVoltageList)

