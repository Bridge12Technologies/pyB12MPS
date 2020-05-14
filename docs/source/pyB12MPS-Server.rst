===============
pyB12MPS Server
===============

Server Commands
---------------

Commands beginning and ending in underscore "_" are special commands which are interpreted by the MPS Server. All other commands are passed directly to the Bridge12 MPS through the serial connection.

+---------------------+------------------------------------------------------+
|Command              |Description                                           |
+=====================+======================================================+
|_close_              |Close the serial port                                 |
+---------------------+------------------------------------------------------+
|_flush_              |Flush the serial port buffer                          |
+---------------------+------------------------------------------------------+
|_in_waiting_         |Return bytes in waiting at serial port                |
+---------------------+------------------------------------------------------+
|_init_               |Initialize MPS serial port connection                 |
+---------------------+------------------------------------------------------+
|_is_system_ready_    |System ready status of MPS (1 = Ready, 0 = Not Ready) |
+---------------------+------------------------------------------------------+
|_stop_               |Stop the MPS Server                                   |
+---------------------+------------------------------------------------------+

Server and Handler Class
------------------------

.. automodule:: pyB12MPS.pyB12MPS_server
   :members:

Example - pyB12MPS Server
-------------------------

Here is an example using functions for checking the status of the MPS server.

.. code-block:: python

    import pyB12MPS as mps

    # Start the server
    mps.start()

    # Test server connection
    testValue = mps.test()

    if testValue == 0:
        print('Server Running')
    else:
        print('Server Error')

    # Test if MPS is ready
    readyValue = mps.systemReady()

    if readyValue == 1:
        print('MPS System is Ready')
    else:
        print('MPS System Not Ready')

    # Stop the server
    mps.stop()


    
