# rpc_using_thrift

Have 2 thrift server instance running, each having a file at
their possession(passed as parameter).  Say a.txt and b.txt.  when a client makes a call to
Server A, A should remove last 10 lines from a.txt and then pass it on
to server B.  server B should prepend the incoming data to b.txt.

client --------> Server A ------> Server B
       <-----------|<----------------|


Requirements :
1. thrift0.9.2
2. python2.7

How to Use:
1. First clone all this files to a folder
2. then run :> thrift --gen py MultiServer.thrift
3. then run both servers and client and you can see changes occur in a.txt and b.txt
