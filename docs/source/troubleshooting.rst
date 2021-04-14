===============
Troubleshooting
===============

----------------------
Server Failed to Start
----------------------

Starting the Server
-------------------

In a terminal start the server by running:

.. code-block:: python
    
    mps.start(debug = True)

This command will start the server in a separate window. All commands sent to and from the server will now be displayed in this window. If the window fails to start, make sure the server has been stopped with the `mps.stop()` command.

The MPS serial port should automatically be detected. If automatic detection fails, make sure the MPS is connected to the computer through the USB interface. If the automatic detection still fails, you may need to manually select the serial port. For example, if the MPS is connected to COM port 3 (COM3):

.. code-block:: python
    
    mps.start('COM3', debug = True)

It may also be the case the the server is unable to initialize on the default port. In this case you may need to manually set the server port:

.. code-block:: python
    
    mps.start(host = 'localhost', port = 50001, debug = True)

Once the connection has been established, you can use the client script to send commands to the MPS.






