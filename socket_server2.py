# encoding:utf-8
import socket
import sys
from pymouse import PyMouse
# import thread
import json

HOST = ''    # Symbolic name meaning all available interfaces
PORT = 10002  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'


conn, addr = s.accept()
print 'A New Connected with ' + addr[0] + ':' + str(addr[1])


def clickmouse(content):
    global m
    x = m.position()[0]
    y = m.position()[1]

    if content == 'left':
        m.click(x, y, 1)
    else:
        m.click(x, y, 2)


def movemouse(content):
    global m
    xy = content.split(',')
    offset_x = int(xy[0])
    offset_y = int(xy[1])
    print "move " + str(offset_x) + "," + str(offset_y)

    x = m.position()[0]
    y = m.position()[1]
    m.move(x + offset_x, y + offset_y)

operate = {'click': clickmouse, 'move': movemouse, }
m = PyMouse()


while 1:
        # wait to accept a connection - blocking call
    data = conn.recv(1024)
    reply = 'OK...' + data
    data = data.split('#')
    print data
    # data = json.loads(data)
    for d in data[0:-1]:
        d = json.loads(d)
        method = d.get('method')
        content = d.get('content')
        print method + content
        operate[method](content)

    # print data
    # conn.sendall(reply)

conn.close()
s.close()
