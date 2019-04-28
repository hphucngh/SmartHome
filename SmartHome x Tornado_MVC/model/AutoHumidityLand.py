import datetime
import json
import RPi.GPIO as GPIO
import threading
import BaseHandler
from bson.json_util import dumps
from config import Env


class AutoHumidityLand(BaseHandler.BaseHandler):
    @tornado.web.authenticated
    def post(self):
        global stop_thread
        pinSoilSensor = 25
        pinWater = 9
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinSoilSensor, GPIO.IN)
        GPIO.setup(pinWater, GPIO.OUT)
        key = self.get_argument("key")
        status = self.get_argument("value")

        def autoWaterTree():
            while 1:
                HumidityLand = GPIO.input(pinSoilSensor)
                if HumidityLand == 1:
                    GPIO.output(pinWater, GPIO.LOW)
                elif HumidityLand == 0:
                    GPIO.output(pinWater, GPIO.HIGH)
                if stop_thread:
                    GPIO.output(pinWater, GPIO.HIGH)
                    break

        if key == "auto-humidity-land":
            if status == "on":
                stop_thread = False
                starttime = datetime.datetime.utcnow()
                threadAutoWater = threading.Thread(target=autoWaterTree)
                threadAutoWater.start()
                new_status = {
                    "name": key,
                    "status": status,
                    "data": "auto device",
                    "starttime": starttime,
                    "endtime": None,
                    "iddevice": "autoHumidityLand",
                }
                Env.database["statusdb"].insert(
                    new_status
                )

                keyWater = "water-tree"
                iddevice = "waterTree"
                data = "on water tree"
                new_status = {
                    "name": keyWater,
                    "status": status,
                    "data": data,
                    "starttime": starttime,
                    "endtime": None,
                    "iddevice": iddevice,
                }
                Env.database["statusdb"].insert(
                    new_status
                )

            if status == "off":
                stop_thread = True
                GPIO.output(pinWater, GPIO.HIGH)
                endtime = datetime.datetime.utcnow()
                finds = json.loads(
                    dumps(
                        Env.database["statusdb"]
                        .find(
                            {"name": key},
                            {
                                "status": 1,
                                "_id": 0,
                            },
                        )
                        .sort([("_id", -1)])
                        .limit(1)
                    )
                )[0]

                f = finds["status"]
                Env.database["statusdb"].update(
                    {"name": key, "status": f},
                    {
                        "$set": {
                            "endtime": endtime,
                            "status": status,
                        }
                    },
                )

                keyWater = "water-tree"
                finds = json.loads(
                    dumps(
                        Env.database["statusdb"]
                        .find(
                            {"name": keyWater},
                            {
                                "status": 1,
                                "_id": 0,
                            },
                        )
                        .sort([("_id", -1)])
                        .limit(1)
                    )
                )[0]
                f = finds["status"]
                Env.database["statusdb"].update(
                    {
                        "name": keyWater,
                        "status": f,
                    },
                    {
                        "$set": {
                            "endtime": endtime,
                            "status": status,
                        }
                    },
                )

