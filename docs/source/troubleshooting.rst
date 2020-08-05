===============
Troubleshooting
===============

----------------------
Server Failed to Start
----------------------

If you received the following error:

.. code-block:: console

    mps.start()
    Server starting...
    Server Error Code: 61
    Server failed to start.


This is due to the server trying to use a port, which is already used by another system process. The pyB12MPS package by default uses port 50007. If this port is already used you can specify a port manually. Try starting the mps server with a different port using:

.. code-block:: console

    import pyB12MPS as mps
    mps.start(port = 12345)


This will start the server using port 12345.


