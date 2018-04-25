from socket import *
from json import *
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.properties import NumericProperty, ReferenceListProperty,ObjectProperty
from kivy.vector import Vector

sk = socket(AF_INET, SOCK_STREAM)
ADDR=('127.0.0.1', 10090)
sk.connect(ADDR)
databuf={}
databuf['type']='playerInit'
databuf['playerid']=10001
msgbuf={}
msgbuf['method']='post'
msgbuf['data']=databuf
msgstr = dumps(msgbuf)
sk.send(msgstr)
recvbuf = sk.recv(4096)
print recvbuf
jsrecv = loads(recvbuf)
map = jsrecv['data']['mapinfo']


class Player(Widget):
    ve_x=NumericProperty(0)
    ve_y=NumericProperty(0)

    velocity=ReferenceListProperty(ve_x,ve_y)

    def move(self):
        self.pos=Vector(*self.velocity) + self.pos

class Game(Widget):
    player=ObjectProperty(None)
    def init_player(self, vel=(4, 0)):
        self.color=(500,1,1)
        self.player=Player()
        self.player.center=self.center
        self.player.velocity=vel
        self.player.color=(300,1,1)

    def update(self, dt):
        self.init_player(vel=(4, 0))
        self.player.move()

class UiApp(App):
    def build(self):
        return Game()

UiApp().run()

