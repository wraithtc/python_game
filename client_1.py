from socket import *
from json import *
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.properties import NumericProperty, ReferenceListProperty,ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window

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
map_width = map['width']
map_height = map['height']

class WidgetDrawer(Widget):
    def __init__(self, imageStr, **kwargs):
        super(WidgetDrawer,self).__init__(**kwargs)

        with self.canvas:
            #self.size = (Window.width, Window.width)
            self.rect_bg=Rectangle(source=imageStr, pos=self.pos,size=self.size)
            self.bind(pos=self.upgrade_graphics_pos)
            self.x=self.center_x
            self.y=self.center_y
            self.pos=(self.x,self.y)
            self.rect_bg.pos=self.pos

    def upgrade_graphics_pos(self, instance, value):
        self.rect_bg.pos = value 

    def setSize(self, width, height):
        self.size=(width, height)
        self.rect_bg.size = (width,height)

    def setPos(self, xPos, yPos):
        self.x = xPos
        self.y = yPos

class ElementAction(Widget):
    def __init__(self, **kwargs):
        super(ElementAction, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self,
                                                'text')
        if self._keyboard.widget:
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('key', keycode, 'have been pressed')
        print('- text is %r' % text)  
        print('- modifiers are %r' % modifiers)

        if keycode[1] == 'escape':
            keboard.release()

        return True

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard=None


class Weapon(WidgetDrawer):
    attack = NumericProperty(0)
    skill = NumericProperty(0)
    
    

        

class Player(WidgetDrawer, ElementAction):
    ve_x=NumericProperty(0)
    ve_y=NumericProperty(0)
    weapon_pos_x = NumericProperty(0)
    weapon_pos_y = NumericProperty(0)

    def move(self, direction):
        if (direction == 0):
            self.x = self.x + self.ve_x 
            self.y = self.y   + 0
        elif (direction == 1):
            self.x = self.x - self.ve_x 
            self.y = self.y   + 0

        elif direction == 2:
            self.x = self.x
            self.y = self.y + self.ve_y

        elif direction == 3:
            self.x = self.x
            self.y = self.y - self.ve_y 

        self.pos = (self.x, self.y)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode[1])
        if keycode[1] == 'd':
            print('move right!')
            self.move(0)
        elif keycode[1] == 'a':
            print('move left!')
            self.move(1)
        elif keycode[1] == 'w':
            print('move up')
            self.move(2)
        elif keycode[1] == 's':
            print('move down')
            self.move(3)
        elif keycode[1] == 'j':
            print('pick weapon!')
            self.pick_weapon()
        else:
            print('invalid key!')

    def pick_weapon(self):
        self.weapon = Weapon(imageStr='./guo.png')
        self.weapon.setSize(30, 10)
        self.weapon_pox_x = self.pos[0]+self.size[0]
        self.weapon_pos_y = self.pos[1]+self.size[1]/2
        print('weapon pos:',self.weapon_pos_x,',',self.weapon_pos_y,
              'size:',self.size[0],',', self.size[1],'pos:',
              self.pos[0],self.pos[1])
        self.weapon.setPos(self.weapon_pos_x, self.weapon_pos_y)
        self.add_widget(self.weapon)


class Game(WidgetDrawer):
    def __init__(self,  **kwargs):
        super(Game, self).__init__(imageStr="./2.jpg", **kwargs)
        self.setSize(map_width, map_height)
        self.setPos(0, 0)
        self.player=Player(imageStr="./1.png")
        #self.player.center=self.center
        self.player.ve_x = 5
        self.player.ve_y = 5
        self.player.setSize(50, 50)
        self.player.setPos(200, 200)
        self.add_widget(self.player)

    def update(self, dt):
        self.player.move()

class UiApp(App):
    def build(self):
        self.parent=Widget()
        self.app=Game()
        #self.player=Player("./1.png")
        #self.player.velocity=(4, 0)
        #self.player.setSize(100, 100)
        #self.player.setPos(200, 200)
        #self.add_widget(self.player)
        #Clock.unschedule(self.app.update)
        #Clock.schedule_interval(self.app.update, 1.0/60.0)
        self.parent.add_widget(self.app)
        #self.parent.add_widget(self.player)
        return self.parent

UiApp().run()

