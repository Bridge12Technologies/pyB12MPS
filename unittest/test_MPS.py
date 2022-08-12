import unittest
import pyB12MPS
import numpy as np

test_power = 1
test_freq = 9.5

class TestMPS(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.mps = pyB12MPS.MPS()

    def test_ampgain(self):
        self.mps.ampgain()

    def test_ampstatus(self):
        self.mps.ampstatus()

    def test_amptemp(self):
        self.mps.amptemp()

    def test_firmware(self):
        self.mps.firmware()

    def test_flush(self):
        self.mps.flush()

    def test_freq(self):
        self.mps.freq(test_freq)
        freq = self.mps.freq()
        self.assertEqual(freq, test_freq)

    def test_id(self):
        self.mps.id()

    def in_waiting(self):
        self.mps.in_waiting()

    def test_lockstatus(self):
        self.mps.lockstatus()

    def test_lockdelay(self):
        self.mps.lockdelay()

    def test_lockstep(self):
        self.mps.lockstep()

    def test_power(self):
        self.mps.power(test_power)
        power = self.mps.power()
        self.assertEqual(power, test_power)

    def test_rfstatus(self):
        self.mps.rfstatus(0)
        rfstatus = self.mps.rfstatus()
        self.assertEqual(rfstatus, 0)

    def test_rxdiodesn(self):
        self.mps.rxdiodesn()

    def test_rxpowerdbm(self):
        self.mps.rxpowerdbm()

    def test_rxpowermv(self):
        self.mps.rxpowermv()

    def test_screen(self):
        self.mps.screen()

    def test_serialNumber(self):
        self.mps.serialNumber()

    def test_systemstatus(self):
        self.mps.systemstatus()

    def trig(self):
        self.mps.trig()

    def triglength(self):
        self.mps.triglength()

    def txdiodesn(self):
        self.mps.txdiodesn()

    def txpowerdbm(self):
        self.mps.txpowerdbm()

    def txpowermv(self):
        self.mps.txpowermv()

    def test_wgstatus(self):
        self.mps.wgstatus(0)
        wgstatus = self.mps.wgstatus()
        self.assertEqual(wgstatus, 0)

    @classmethod
    def tearDownClass(self):
        self.mps.close()

if __name__ == "__main__":
    pass

