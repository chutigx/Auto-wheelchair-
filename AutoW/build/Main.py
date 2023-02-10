import time
from Presenter.ControlPresenter import *
from Presenter.CallPresenter import *
from Presenter.ScanPresenter import *
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window
from kivy.config import Config
from kivy.properties import DictProperty

Config.set('graphics', 'width', '375')
Config.set('graphics', 'height', '812')
Window.size = (375, 812)

Builder.load_file('View/Home.kv')


class HomeScreen(MDScreen):
    @staticmethod
    def showPin(x):
        while x < 1:
            time.sleep(1)
            x = x - 10
            print(x)
        return "Tình trạng pin: " + str(x) + "%"
    pass


class ScanScreen(MDScreen):
    def scanDeivce(self):
        ScanWheelChairs.scanDeivce()
    pass


class ControlScreen(MDScreen):
    def MoveLeft(self):
        Control.MoveLeft(self)

    def MoveRight(self):
        Control.MoveRight(self)

    def MoveForward(self):
        Control.MoveForward(self)

    def MoveBackward(self):
        Control.MoveBackward(self)

    def Stop(self):
        Control.Stop(self)

    def BatteryNofication(self):
        Control.BatteryNofication(self)
    pass


class CallScreen(MDScreen):
    def Start(self):
        CallWheelChair.Start(self)
    def GoBackToParking(self):
        CallWheelChair.GoBackToParking(self)

    pass


class MainApp(MDApp):
    data = DictProperty()

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.sm = MDScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(ScanScreen(name='scanDevice'))
        self.sm.add_widget(ControlScreen(name='controlScreen'))
        self.sm.add_widget(CallScreen(name='callScreen'))
        self.data = {
            '1: Nhà vệ sinh': [
                'toilet',
                "on_press", lambda x: print("pressed toilet"),

            ],
            '2: Phòng chờ': [
                'sofa-single-outline',
                "on_press", lambda x: print("pressed Phòng chờ"),

            ],
            '3: Vị trí lên máy bay 1': [
                'airplane-takeoff',
                "on_press", lambda x: print("pressed Vị trí lên máy bay"),
            ],
        }
        return self.sm
        # return
        # Builder.load_string('Screen.kv')


MainApp().run()
