# encoding=utf-8
# disigned by kidy zhang

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


class MouseWork(PyMouse):

    """docstring for MouseWork"""

    def __init__(self):
        # self.content = content
        self.method = {'click': self.clickmouse,
                       'move': self.movemouse}

    def clickmouse(self, content):
        self.x = self.position()[0]
        self.y = self.position()[1]
        if content == 'left':
            self.click(self.x, self.y, 1)
        else:
            self.click(self.x, self.y, 2)

    def movemouse(self, content):
        self.x = self.position()[0]
        self.y = self.position()[1]
        xy = content.split(',')
        offset_x = int(xy[0])
        offset_y = int(xy[1])
        self.move(self.x + offset_x, self.y + offset_y)

conn, addr = s.accept()  # accept a connnection
print 'A New Connected with ' + addr[0] + ':' + str(addr[1])


mymouse = MouseWork()

while 1:
    data = conn.recv(2048)  # 目前限定最大一次获取2048个字符数据
    data = data.split('#')  # every data is splited by '#'
    for d in data[0:-1]:
        d = json.loads(d)   # loads json
        method = d.get('method')
        content = d.get('content')
        mymouse.method[method](content)

# while 1:
    # now keep talking with the client
    # mouse = thread.start_new_thread(pymouse_action, (conn,))
    # 一个多线程的设计

s.close()
