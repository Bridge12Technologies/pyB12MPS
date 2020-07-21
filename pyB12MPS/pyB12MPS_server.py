import numpy as np

import serial
import time

import socket
import serial.tools.list_ports

try:
    import SocketServer
except:
    import socketserver as SocketServer

import sys

import os
import sys

# Add file path so that serverConfig can be imported from same directory as script
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
sys.path.append(dir_path)

import serverConfig

defaultSerialPort = serverConfig.defaultSerialPort

print('Running Server Initialization Script...')

autoDetectSerialPort = serverConfig.autoDetectSerialPort

initializeOnStart = serverConfig.initializeOnStart

numArguments = len(sys.argv) - 1

print('Number of arguments: ' + str(numArguments))

if numArguments > 0:
    argumentSerialPort = sys.argv[1]
    print('Received Serial Port Argument: %s'%argumentSerialPort)

systemReadyString = serverConfig.systemReadyString

class MPSTCPServer(SocketServer.TCPServer):
    '''Server for MPS Communication
    '''
    def __init__(self,ip_port,MPSTCPHandler):
        SocketServer.TCPServer.__init__(self, ip_port, MPSTCPHandler)

        self.is_system_ready = False
        if numArguments > 0:
            self.serialPort = argumentSerialPort
        elif autoDetectSerialPort:
            self.serialPort = self.detectSerialPort()
        else:
            self.serialPort = defaultSerialPort

    def detectSerialPort(self):
        '''Automatically Detect Serial Port for MPS
        '''
        print('Automatically Detecting Serial Port...')
        ports = list(serial.tools.list_ports.comports())
        arduinoDetected = False
        for p in ports:
            print(p)
            if 'Arduino' in p.description:
                arduinoDetected = True
                arduinoPort = p.device
                print('MPS Detected on port %s'%(arduinoPort))
        if arduinoDetected:
            serialPort = arduinoPort
        else:
            print('No MPS automatically detected. Trying %s instead (default COM port)'%(defaultSerialPort))
            serialPort = defaultSerialPort 
        return serialPort

    def initializeMPS(self):
        '''Initialize the MPS serial connection
        '''
        if self.is_system_ready == True:
            self.closeMPS()

        print('Using Serial Port: ' + self.serialPort)
        self.ser = serial.Serial(self.serialPort,115200,timeout = 1.)
        time.sleep(0.1)
        while not self.is_system_ready:
            time.sleep(0.1)
            bytes_in_waiting = self.ser.in_waiting
            if bytes_in_waiting > 0:
                read_bytes = self.ser.readline()
                read_string = read_bytes.decode('utf-8').rstrip()
                print(read_string)
                if read_string == systemReadyString:
                    self.is_system_ready = True
        time.sleep(0.1)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()


    def closeMPS(self):
        '''Close the MPS serial port
        '''
        self.ser.close()
        self.is_system_ready = False

class MPSTCPHandler(SocketServer.BaseRequestHandler):
    """The RequestHandler class for MPS server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def __init__(self,request,client_address,server):
        SocketServer.BaseRequestHandler.__init__(self,request,client_address,server)

    def handle(self):
        # self.request is the TCP socket connected to the client
        recv_bytes = self.request.recv(1024)
        recv_string = recv_bytes.decode('utf-8').rstrip()

        ### special commands for serial port ###
        if recv_string == '_flush_':
            print('Flushing Buffer')
            self.server.ser.reset_input_buffer()
            self.server.ser.reset_output_buffer()
        elif recv_string == '_in_waiting_':
            value = self.server.ser.in_waiting
            print('Returning bytes "in waiting": %i'%value)
            value_string = str(value) + '\n'
            value_bytes = value_string.encode('utf-8')
            self.request.sendall(value_bytes)
        elif recv_string == '_close_':
            self.server.ser.close()
            self.server.closeMPS()
            print('Closed serial port.')
        elif recv_string == '_init_':
            print('Initializing MPS...')
            self.server.initializeMPS()
        elif recv_string == '_is_system_ready_':
            isMPSReady_bool = self.server.is_system_ready
            isMPSReady_int = int(isMPSReady_bool)
            isMPSReady_string = str(isMPSReady_int) + '\n'
            isMPSReady_bytes = isMPSReady_string.encode('utf-8')
            self.request.sendall(isMPSReady_bytes)

        elif recv_string == '_stop_':
            print('Stopping Server...')
            self.server._BaseServer__shutdown_request = True

        ### MPS Commands ###
        elif self.server.is_system_ready == True:
            print('Sending to MPS: ' + recv_string)

            self.server.ser.write(recv_bytes)

            # if query
            if recv_string[-1] == '?':
                # Read the serial data
                from_mps_bytes = self.server.ser.readline()
                from_mps_string = from_mps_bytes.decode('utf-8').rstrip()
                print('Query Detected, sending to client: ' + from_mps_string)
                self.request.sendall(from_mps_bytes)
            # if non-query, check for bytes in buffer (checking for 'ERROR\n')
            else:
                bytes_in_buffer = self.server.ser.in_waiting
                if bytes_in_buffer > 0:
                    from_mps_bytes = self.server.ser.read(bytes_in_buffer)
                    from_mps_string = from_mps_bytes.decode('uft-8').rstrip()
                    print('Unsolicited Response: ' + from_mps_string)



HOST = serverConfig.HOST
PORT = serverConfig.PORT

if __name__ == '__main__':
    print('Starting Server...')
    server = MPSTCPServer((HOST, PORT), MPSTCPHandler)
    server.serve_forever()
    server.server_close()
    print('Done.')
