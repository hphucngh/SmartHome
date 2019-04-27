import datetime
import json
import threading
import time
import BaseHandler
import RPi.GPIO as GPIO
import tornado.web
from bson.json_util import dumps
from config import Env

class AutoClothesline(BaseHandler.BaseHandler):
    @tornado.web.authenticated
    def post(self):
        global stop_thread

        pinRainSensor = 12
        pinClothesline = 21

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(pinRainSensor, GPIO.IN)
        GPIO.setup(pinClothesline, GPIO.OUT)

        key = self.get_argument("key")
        status = self.get_argument("value")

        def autoClothesline():
            ServoRain = GPIO.PWM(pinClothesline, 50)
            ServoRain.start(11.5)
            while (1):
                Rain = GPIO.input(pinRainSensor)
                if (Rain == 0):
                    ServoRain.start(11.5)
                    ServoRain.ChangeDutyCycle(2.5)
                    time.sleep(1.5)
                elif (Rain == 1):
                    ServoRain.start(2.5)
                    ServoRain.ChangeDutyCycle(11.5)
                    time.sleep(1.5)
                if stop_thread:
                    ServoRain.start(11.5)
                    ServoRain.ChangeDutyCycle(2.5)
                    time.sleep(1.5)
                    GPIO.output(pinClothesline, False)
                    ServoRain.ChangeDutyCycle(0)
                    ServoRain.stop()
                    break

        if key == "auto-clothesline":
            if status == "on":
                stop_thread = False
                starttime = datetime.datetime.utcnow()
                threadAutoClothesline = threading.Thread(target=autoClothesline)
                threadAutoClothesline.start()
                new_status = {
                    "name": key,
                    "status": status,
                    "data": "auto device",
                    "starttime": starttime,
                    "endtime": None,
                    "iddevice": "autoClothesline"
                }
                Env.database["statusdb"].insert(new_status)

                keyClothesline = "clothesline"
                iddevice = "clothesline"
                data = "on clothesline"

                new_status = {
                    "name": keyClothesline,
                    "status": status,
                    "data": data,
                    "starttime": starttime,
                    "endtime": None,
                    "iddevice": iddevice
                }
                Env.database["statusdb"].insert(new_status)

            if status == "off":
                stop_thread = True
                endtime = datetime.datetime.utcnow()
                finds = json.loads(dumps(
                    Env.database["statusdb"].find({"name": key}, {"status": 1, "_id": 0}).sort([("_id", -1)]).limit(
                        1)))[0]

                f = finds["status"]
                Env.database["statusdb"].update({"name": key, "status": f},
                                                {"$set": {"endtime": endtime, "status": status}})

                keyClothesline = "clothesline"
                finds = json.loads(dumps(
                    Env.database["statusdb"].find({"name": keyClothesline}, {"status": 1, "_id": 0}).sort(
                        [("_id", -1)]).limit(1)))[0]
                f = finds["status"]
                Env.database["statusdb"].update({"name": keyClothesline, "status": f},
                                                {"$set": {"endtime": endtime, "status": status}})
