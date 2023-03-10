===============
Troubleshooting
===============


Connecting to MPS
-----------------

The MPS serial port should automatically be detected. If automatic detection fails, make sure the MPS is connected to the computer through the USB interface. If the automatic detection still fails, you may need to manually select the serial port. For example, if the MPS is connected to COM port 3 (COM3):

.. code-block:: python
    
    mps = pyB12MPS.MPS('COM3')

