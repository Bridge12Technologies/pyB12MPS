=================
Quick-Start Guide
=================

--------
Overview
--------

The pyB12MPS package consists of an MPS Class:
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

    import pyB12MPS

    mps = pyB12MPS.MPS()

The pyB12MPS module contains the MPS class. When the MPS class is initialized, a serial port is opened to communicate with the MPS.

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

    mps.close()
    # closes the serial port and stops communication with the MPS
    del mps
    # deletes the instance of the class

This will stop the serial communication with the system.

Sending MPS Commands
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

    import pyB12MPS
    import time

    # Initialize MPS Class
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

        # Append voltage reading to list
        rxVoltageList.append(rxVoltage)

    # print result
    print('Rx Voltage Readings:')
    print(rxVoltageList)

