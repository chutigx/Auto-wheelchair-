from kivy.network.urlrequest import UrlRequest


class Control:
    def MoveLeft(self):
        UrlRequest('http://192.168.1.184:80/trai')
        print("trai")

    def MoveRight(self):
        UrlRequest('http://192.168.1.199:80/phai')
        print("phai")

    def MoveForward(self):
        UrlRequest('http://192.168.1.199:80/toi')
        print("toi")

    def MoveBackward(self):
        UrlRequest('http://192.168.1.199:80/lui')
        print("lui")

    def Stop(self):
        UrlRequest('http://192.168.1.199:80/dung')
        print("dung")

    def BatteryNofication(self):
        print("%")