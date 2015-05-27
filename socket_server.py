import socket
import sys
from pymouse import PyMouse

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8789 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
s.listen(10)
print 'Socket now listening'
 
conn, addr = s.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])
#now keep talking with the client
m = PyMouse()

while 1:
    #wait to accept a connection - blocking call   
    data = conn.recv(1024)
    reply = 'OK...' + data
    data = data.split(',')
    offset_x = int(data[0])
    offset_y = int(data[1])
    print str(offset_x) + str(offset_y)
    x = m.position()[0]
    y = m.position()[1]
    m.move(x + offset_x , y + offset_y)
     
    conn.sendall(reply)
 
conn.close()
s.close()