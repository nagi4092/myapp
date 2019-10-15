from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager,Screen,NoTransition,SlideTransition
from kivy.properties import ObjectProperty,ListProperty,StringProperty,NumericProperty

path = "kv/property.kv"
Builder.load_file(path)
Config.set("graphics","resizable",True)
Config.set("graphics","width",1280)
Config.set("graphics","height",720)
#Config.set('graphics', 'window_state', 'maximized')


traffic_setup = ["\tpinMode(2,OUTPUT);\n","\tpinMode(3,OUTPUT);\n","\tpinMode(4,OUTPUT);\n"]
traffic_code = []
t_code_buf = []


import os
import build as core

class Coder_t(Screen):
    def __init__(self,**kwargs):
        super(Coder_t,self).__init__(**kwargs)
        pass
    
    all = ListProperty()

    console = ObjectProperty(None)
    slider = ObjectProperty(None)
    sl_btn = ObjectProperty(None)

    count = 1
    def printcsl(self,arg):
        if self.count < 10:
            data = str(self.count) + ".    " + arg
        elif 10 <= self.count & self.count <100:
            data = str(self.count) + ".  " + arg
        else:
            data = str(self.count) + "." + arg

        self.all.append(data)
        self.console.text = "\n".join(self.all) + "\n"
        self.count += 1

    def ev_slider(self,*arg):
        self.sl_btn.text = str('{:.0f}'.format(int(self.slider.value))) + " sec waiting"
        pass
    
    def set_transition(self):
        self.manager.transition = SlideTransition()
        self.manager.transition.duration = 0.6
        self.manager.transition.direction = "down"

    def build(self,*arg):
        global traffic_code,traffic_setup
        core.builder(traffic_setup,traffic_code)
        #core.call_compiler()

    def ev_btn(self,state,id):#--test
        global traffic_code
        if state == "down" and id == 1:
            traffic_code.append("\tdigitalWrite(2,HIGH);\n")
            self.printcsl("Blue LED ON")
        elif state == "down" and id == 2:
            traffic_code.append("\tdigitalWrite(3,HIGH);\n")
            self.printcsl("Yelow LED ON")
        elif state == "down" and id == 3:
            traffic_code.append("\tdigitalWrite(4,HIGH);\n")
            self.printcsl("Red LED ON")
        if state == "normal":
            if id == 1:
                traffic_code.append("\tdigitalWrite(2,LOW);\n")
                self.printcsl("Blue LED OFF")
            elif id == 2:
                traffic_code.append("\tdigitalWrite(3,LOW);\n")
                self.printcsl("Yelow LED OFF")
            elif id == 3:
                traffic_code.append("\tdigitalWrite(4,LOW);\n")
                self.printcsl("Red LED OFF")

        print(state)
        print(traffic_code)

    def ev_reset(self):
        global traffic_code
        traffic_code.clear()
        self.all.clear()
        self.count = 1
        self.console.text = ""
        print(traffic_code)

        

    def ev_slbtn(self,value,text):
        global traffic_code
        self.printcsl(text)
        traffic_code.append("\tdelay("+str(value)+"000);\n")
        

        
        
class Simulator(Screen):
    def __init__(self,**kwargs):
        super(Simulator,self).__init__(**kwargs)
        pass

class Slide(Screen):
    source = StringProperty("")

    image = ObjectProperty(None)
    next_btn = ObjectProperty(None)
    num_of_pages = ObjectProperty(None)

    directory = ""
    pages = 0

    def __init__(self,dir_name = "./image",**kwargs):
        super(Slide,self).__init__(**kwargs)
        self.directory = dir_name
        self.get_filepath(self.directory)
        self.source = os.path.join(self.directory,self.filepath[0])
        pass

    def get_filepath(self,dir_name):
        self.filepath = os.listdir(self.directory)

    def next(self,*arg):
        self.pages += 1

        if self.pages == len(self.filepath):
            self.manager.transition.direction = "down"
            self.manager.current = "coder"
            self.pages = 0
            self.source = os.path.join(self.directory,self.filepath[self.pages])
            self.image.reload()
            self.num_of_pages.text = str(int(self.pages + 1))+" page"
            pass

        self.source = os.path.join(self.directory,self.filepath[self.pages])
        self.image.reload()
        self.num_of_pages.text = str(int(self.pages + 1))+" page"

    def back(self,*arg):
        if self.pages == 0:
            return
        self.pages -= 1 
        
        self.source = os.path.join(self.directory,self.filepath[self.pages])
        self.image.reload()
        self.num_of_pages.text = str(int(self.pages + 1))+" page"

    def change_text(self):
        if self.pages == len(self.filepath)-1:
            self.next_btn.text = "END"
        else:
            self.next_btn.text = "next"

    

class Select(Screen):

    tr_btn = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(Select,self).__init__(**kwargs)

    def set_screen(self):
        if self.tr_btn.text == "traffic":
            self.coder = Coder_t(name = "coder")
            self.slide = Slide(name = "slide",dir_name = "./image")
        


class MainApp(App):
    def __init__(self,**kwargs):
        super(MainApp,self).__init__(**kwargs)
        self.title = 'MuffinTime'
        self.use_kivy_settings = False
    
    def build(self):            #make widget tree and associate kivy
        self.sm = ScreenManager()        
        self.sm.add_widget(Select(name = "select"))
        self.sm.add_widget(Simulator(name = "simulator"))
        return self.sm
        

if __name__ == '__main__':
    
    MainApp().run()
