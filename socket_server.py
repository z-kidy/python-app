import socket
import sys
from pymouse import PyMouse
import thread

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8885 # Arbitrary non-privileged port
 
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

def pymouse_action(conn):        
    while 1:
        #wait to accept a connection - blocking call   
        data = conn.recv(1024)
        reply = 'OK...' + data
        data = data.split(',')
        offset_x = int(data[0])
        offset_y = int(data[1])
        print "move "+str(offset_x) + "," + str(offset_y)
        m = PyMouse()
        x = m.position()[0]
        y = m.position()[1]
        m.move(x + offset_x , y + offset_y)
         
        conn.sendall(reply)
 
    conn.close()

while 1: 
    conn, addr = s.accept()
    print 'A New Connected with ' + addr[0] + ':' + str(addr[1])
    #now keep talking with the client
    mouse = thread.start_new_thread(pymouse_action, (conn,) )


s.close()