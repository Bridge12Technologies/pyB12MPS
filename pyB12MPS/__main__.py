import argparse
import time

import serial

try:
    import SocketServer
except:
    import socketserver as SocketServer


parser = argparse.ArgumentParser()
parser.add_argument('serialport', help = 'MPS Serial Port')
parser.add_argument('host', help = 'IP for TCP Server')
parser.add_argument('port', help = 'port for TCP Server')
#
args = parser.parse_args()
print(args)

# Server Parameters
serialPort = args.serialport
HOST = args.host
PORT = int(args.port)

print('serialPort: %s'%serialPort)
print('HOST: %s'%HOST)
print('PORT: %s'%PORT)

class MPSTCPServer(SocketServer.TCPServer):
    '''Server for MPS Communication
    '''
    def __init__(self,ip_port,MPSTCPHandler):
        SocketServer.TCPServer.__init__(self, ip_port, MPSTCPHandler)

        self.is_system_ready = False
        self.serialPort = serialPort
        print('Server Initialized.')

    def initializeMPS(self):
        '''Initialize the MPS serial connection
        '''
        if hasattr(self, 'ser'):
            self.closeMPS()

        print('Using Serial Port: ' + self.serialPort)
        self.ser = serial.Serial(self.serialPort,115200,timeout = 1.)

        time.sleep(0.1)
        read_string = ''
        while read_string != 'System Ready':
            time.sleep(0.1)
            bytes_in_waiting = self.ser.in_waiting
            if bytes_in_waiting > 0:
                read_bytes = self.ser.readline()
                read_string = read_bytes.decode('utf-8').rstrip()
                print(read_string)
        time.sleep(0.5)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        print('Done.')

    def closeMPS(self):
        '''Close the MPS serial port
        '''
        self.ser.close()
        del self.ser

    def systemReady(self):
        return hasattr(self, 'ser')

class MPSTCPHandler(SocketServer.BaseRequestHandler):
    """The RequestHandler class for MPS server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def __init__(self,request,client_address,server):
        SocketServer.BaseRequestHandler.__init__(self,request,client_address,server)

    def handle(self):
        print()
        print('Receiving from client...')
        # self.request is the TCP socket connected to the client
        recv_bytes = self.request.recv(1024)
        recv_string = recv_bytes.decode('utf-8').rstrip()
        print('Received string: %s'%recv_string)

        ### special commands for serial port ###
        if recv_string == '_flush_':
            print('Flushing Buffer')
            self.server.ser.reset_input_buffer()
            self.server.ser.reset_output_buffer()
            print('Done.')
        elif recv_string == '_in_waiting_':
            value = self.server.ser.in_waiting
            print('Returning bytes "in waiting": %i'%value)
            value_string = str(value) + '\n'
            value_bytes = value_string.encode('utf-8')
            self.request.sendall(value_bytes)
            print('Done.')
        elif recv_string == '_close_':
            print('Closing Serial Port...')
            self.server.ser.close()
            self.server.closeMPS()
            print('Done.')
        elif recv_string == '_init_':
            print('Initializing MPS...')
            self.server.initializeMPS()
            print('Done.')
        elif recv_string == '_is_system_ready_':
            print('Is System Ready?')
            isMPSReady_bool = self.server.systemReady()
            if isMPSReady_bool:
                print('YES')
            else:
                print('NO')
            isMPSReady_int = int(isMPSReady_bool)
            isMPSReady_string = str(isMPSReady_int) + '\n'
            isMPSReady_bytes = isMPSReady_string.encode('utf-8')
            self.request.sendall(isMPSReady_bytes)

        elif recv_string == '_stop_':
            print('Stopping Server...')
            self.server._BaseServer__shutdown_request = True

        elif hasattr(self.server, 'ser'):
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
                    from_mps_string = from_mps_bytes.decode('utf-8').rstrip()
                    print('Unsolicited Response: ' + from_mps_string)

        else:
            print('Invalid Command')



print('Starting Server...')
server = MPSTCPServer((HOST, PORT), MPSTCPHandler)
server.serve_forever()
print('Closing Server...')
server.server_close()
print('Done.')
