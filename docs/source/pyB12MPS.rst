===============
pyB12MPS Module
===============

In this section the methods of the MPS class are explained. In general, most functions can be used to query a parameter, while some functions can query and set (send) a value to the MPS.

For example the command::

   mps.freq()

will return the current microwave frequency of the MPS, while::

   mps.freq(9.554)

will set the microwave frequency to 9.554 GHz.


pyB12MPS Functions
------------------

.. autoclass:: pyB12MPS.MPS
   :members:

Example - pyB12MPS Module
-------------------------

::

    import pyB12MPS

    mps = pyB12MPS.MPS()

    mps.freq(9.6) # Set microwave frequency to 9.6 GHz

    mps.power(10) # Set microwave power to 10 dBm

    mps.close() # Stop the server

