import time
import datetime
import json
import RPi.GPIO as GPIO
import Adafruit_DHT
import threading
import BaseHandler
from bson.json_util import dumps
from config import Env


class OnOffDevice(BaseHandler.BaseHandler):
    @tornado.web.authenticated
    def post(self):
        pinTemperatureHumidity = 26
        pinTemperatureHumidityRoom = 18
        pinFanLivingRoom = 13
        pinFanBedRoom = 19
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinTemperatureHumidity, GPIO.OUT)
        GPIO.setup(pinTemperatureHumidityRoom, GPIO.OUT)
        GPIO.setup(pinFanLivingRoom, GPIO.OUT)
        GPIO.setup(pinFanBedRoom, GPIO.OUT)
        key = self.get_argument("key")
        status = self.get_argument("value")

        def writeTemperatureHumidity():
            sensor = Adafruit_DHT.DHT11
            while True:
                humidity, temperature = Adafruit_DHT.read_retry(sensor, pinTemperatureHumidity)
                if humidity is not None and temperature is not None:
                    new_status = {
                        "name": "temperature-humidity-bedroom",
                        "temperature": temperature,
                        "humidity": humidity,
                        "time": datetime.datetime.utcnow(),
                        "iddevice": "temperaturehumidityBedRoom"
                    }
                    Env.database["statusdb"].insert(
                        new_status
                    )
                    time.sleep(2)
                else:
                    break

        if key == "fan-living-room":
            if status == "on":
                starttime = datetime.datetime.utcnow()  # Cap nhat thoi gian hien tai tren he thong
                GPIO.output(pinFanLivingRoom, GPIO.HIGH)  # Dien ap duoc bat sang che do cao - Quat bat
                self.write("true")  # Tra ve clien "true"
                new_status = {
                    "name": key,
                    "status": status,
                    "data": "on device",
                    "starttime": starttime,
                    "endtime": None,
                    "iddevice": "fanLivingRoom"
                }
                Env.database["statusdb"].insert(
                    new_status
                )  # Insert du lieu new_status vao Collection statusdb

            if status == "off":
                endtime = datetime.datetime.utcnow()  # Cap nhat thoi gian tat thiet bi
                GPIO.output(pinFanLivingRoom, GPIO.LOW)  # Dien ap duoc giam - Quat tat
                self.write("true")  # Tra ve client "true"
                # Tim kiem xem co Document nao co {"name" : key} va loc theo truong "status" => sap xep theo _id va lay 1 document => [0] bo [] trong [{...}] thanh {...}
                finds = json.loads(
                    dumps(
                        Env.database["statusdb"]
                            .find(
                            {
                                "name": key
                            },
                            {
                                "status": 1,
                                "_id": 0
                            }
                        )
                        .sort([("_id", -1)])
                        .limit(1)
                    )
                )[0]

                # Chua bat ngoai le cho truong hop status bang off
                f = finds["status"]
                Env.database["statusdb"].update(
                    {
                        "name": key,
                        "status": f
                    },
                    {
                        "$set": {
                            "endtime": endtime,
                            "status": status
                        }
                    }
                )

        elif key == "fan-bed-room":
            if status == "on":
                starttime = datetime.datetime.utcnow()  # Cap nhat thoi gian hien tai tren he thong
                GPIO.output(pinFanBedRoom, GPIO.HIGH)  # Dien ap duoc bat sang che do cao - Quat bat
                self.write("true")  # Tra ve clien "true"
                new_status = {
                    "name": key,
                    "status": status,
                    "data": "on device",
                    "starttime": starttime,
                    "endtime": None,
                    "iddevice": "fanBedRoom"
                }
                Env.database["statusdb"].insert(
                    new_status
                )  # Insert du lieu new_status vao Collection statusdb

            if status == "off":
                endtime = datetime.datetime.utcnow()  # Cap nhat thoi gian tat thiet bi
                GPIO.output(pinFanBedRoom, GPIO.LOW)  # Dien ap duoc giam - Quat tat
                self.write("true")  # Tra ve client "true"
                # Tim kiem xem co Document nao co {"name" : key} va loc theo truong "status" => sap xep theo _id va lay 1 document => [0] bo [] trong [{...}] thanh {...}
                finds = json.loads(
                    dumps(
                        Env.database["statusdb"]
                            .find(
                            {
                                "name": key
                            },
                            {
                                "status": 1,
                                "_id": 0
                            }
                        )
                        .sort([("_id", -1)])
                        .limit(1)
                    )
                )[0]

                # Chua bat ngoai le cho truong hop status bang off
                f = finds["status"]
                Env.database["statusdb"].update(
                    {
                        "name": key,
                        "status": f
                    },
                    {
                        "$set": {
                            "endtime": endtime,
                            "status": status
                        }
                    }
                )

        elif key == "temperature-humidity-bedroom":
            if status == "on":
                GPIO.output(pinTemperatureHumidityRoom, GPIO.HIGH)
                threadTemperature = threading.Thread(target=writeTemperatureHumidity)
                threadTemperature.start()
            elif status == "off":
                GPIO.output(pinTemperatureHumidityRoom, GPIO.LOW)

