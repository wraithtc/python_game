from socket import *
from time import ctime
from json import *
from threading import *
from gammap import *

host = '127.0.0.1'

port = 10090
buffsize = 4096
ADDR = (host, port)

sk = socket(AF_INET, SOCK_STREAM)

sk.bind(ADDR)
sk.listen(3)

def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    recvBuf = sock.recv(buffsize)
    print('receive msg %s' % recvBuf)
    js=loads(recvBuf)
    if js['data']['type'] != 'playerInit':
        print ('Illegal msg ...')
    else:
        print('got new player, id:%s ...' % js['data']['playerid'])
        map = {'width':800, 'height':800}
        sendbuf = {}
        databuf = {}
        playerinfo = {}
        playerinfo['hp'] = 100
        playerinfo['mana'] = 100
        POS=(0, 0)
        playerinfo['pos'] =POS 
        databuf['type'] = 'gamestart'
        databuf['playerinfo'] = playerinfo
        databuf['mapinfo'] = map 
        sendbuf['method'] = 'post'
        sendbuf['data'] = databuf
        sendstr = dumps(sendbuf)
        sock.send(sendstr)


while True:
    print('server start , wait for conection ...')
    sock,addr = sk.accept()

    t = Thread(target=tcplink, args=(sock, addr))
    t.start()

    


