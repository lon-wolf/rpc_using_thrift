#!/usr/bin/env python

port = 9090
host = "localhost"

import sys
# your gen-py dir
sys.path.append('gen-py')

# MultiServer files
from MultiServer import *
from MultiServer.ttypes import *

# Thrift files
import os
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

def callB(lines):
    try:
        # Init thrift connection and protocol handlers
        transportA = TSocket.TSocket( host , 9080)
        transportA = TTransport.TBufferedTransport(transportA)
        protocolA = TBinaryProtocol.TBinaryProtocol(transportA)

        # Set client to our MultiServer
        clientA = MultiServer.Client(protocolA)

        # Connect to server
        transportA.open()

        s = clientA.ServerB(lines)
        print s

        # Close connection
        transportA.close()

    except Thrift.TException, tx:
        print 'Something went wrong : %s' % (tx.message)
        return "Problem in calling server B"
    return "Server A Done"

# Server implementation
class MultiServerHandler:
    def ServerA(self):
        f = open('a.txt','rw+')
        f.seek(0, os.SEEK_END)
        position = f.tell()
        counter = 0
        while position >= 0:
            f.seek(position)
            if (f.read(1) == '\n'):
                counter += 1
                if (counter == 11):
                    p = f.tell()
                    lines = f.read()
                    f.seek(p)
                    f.truncate()
                    f.close()
                    str = callB(lines)
                    break
            position -= 1
        if (counter < 11):
            return "a.txt is small in size"
        else:
            return str
    
# set handler to our implementation
handler = MultiServerHandler()

processor = MultiServer.Processor(handler)
transport = TSocket.TServerSocket(port = port)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

# set server
server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

print 'Starting server'
server.serve()