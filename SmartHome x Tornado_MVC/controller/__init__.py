import tornado.web
from model import VersionHandler, Login, LightsOnOff, Home, Lights, Profile, ProfileUpdatePersonal, Climate, \
    OnOffDevice, TemperatureHumidity, Reload, ReloadChart, Automatic, AutoFanLivingRoom, AutoLightKitchenRoom, \
    AutoClothesline, AutoHumidityLand, StreamCamera
from config import Env
import os.path
import RPi.GPIO as GPIO
import threading
import time
import datetime

class router:
    def __init__(self):

        self.router = tornado.web.Application([
            (r"/version", VersionHandler),
            (r"/login", Login),
            (r"/home", Home),
            (r"/lights", Lights),
            (r"/profile", Profile),
            (r"/climate", Climate),
            (r"/automatic", Automatic),
            (r"/autofanlivingroom", AutoFanLivingRoom),
            (r"/autolightkitchenroom", AutoLightKitchenRoom),
            (r"/autohumidityland", AutoHumidityLand),
            (r"/autoclothesline", AutoClothesline),
            (r"/profile/update/personal", ProfileUpdatePersonal),
            (r"/lightsonoff", LightsOnOff),
            (r"/onoffdevice", OnOffDevice),
            (r"/temperaturehumidity", TemperatureHumidity),
            (r"/climate/reload", Reload),
            (r"/climate/reloadchart", ReloadChart),
            (r"/streamcamera", StreamCamera)
        ],

            template_path=os.path.join(os.path.dirname(__file__), "../view/templates"),
            static_path=os.path.join(os.path.dirname(__file__), "../view/templates/assets"),
            cookie_secret="x772x",
            login_url="/login"
        )
        self.router.listen(Env.PORT)

    def threadGas(pinGas, pinRed):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinGas, GPIO.IN)
        GPIO.setup(pinRed, GPIO.OUT)
        while (1):
            Gas = GPIO.input(pinGas)
            if (Gas == 0):
                GPIO.output(pinRed, GPIO.HIGH)
                time.sleep(1)
            elif (Gas == 1):
                GPIO.output(pinRed, GPIO.LOW)
                time.sleep(1)

    pinGas = 14
    pinRed = 15
    threadGas = threading.Thread(target=threadGas, args=(pinGas, pinRed,))
    threadGas.start()
