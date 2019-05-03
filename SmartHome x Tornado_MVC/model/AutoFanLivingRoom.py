import tornado.web
import datetime
import json
import threading
import Adafruit_DHT
import BaseHandler
import RPi.GPIO as GPIO
from bson.json_util import dumps
from config import Env


class AutoFanLivingRoom(BaseHandler.BaseHandler):
    @tornado.web.authenticated
    def post(self):
        pinTemperatureHumidity = 26 # GPIO 26 doc nhiet do va do am trong phong
        pinTemperatureHumidityRoom = 18 # GPIO 18 de bat tat cam bien nhiet do, do am trong phong
        pinFanLivingRoom = 13 # GPIO 13 bat tat quat trong Living room
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinTemperatureHumidity, GPIO.OUT)
        GPIO.setup(pinTemperatureHumidityRoom, GPIO.OUT)
        GPIO.setup(pinFanLivingRoom, GPIO.OUT)
        key = self.get_argument("key") # Key : xac dinh thiet bi
        status = self.get_argument("value")	# Trang thai thiet bi

        def autoFanLivingRoom():
            sensor = Adafruit_DHT.DHT11
            while True:
                humidity, temperature = Adafruit_DHT.read_retry(sensor, pinTemperatureHumidity)
                if humidity is not None and temperature is not None:
                    if (temperature > 30):
                        GPIO.output(pinFanLivingRoom, GPIO.HIGH)
                    else:
                        GPIO.output(pinFanLivingRoom, GPIO.LOW)
                else:
                    GPIO.output(pinFanLivingRoom, GPIO.LOW)
                    break

        if key == "auto-fan-living-room":
            if status == "on":
                starttime = datetime.datetime.utcnow()
                GPIO.output(pinTemperatureHumidityRoom, GPIO.HIGH)
                threadAutoFan = threading.Thread(target=autoFanLivingRoom)
                threadAutoFan.start()
                new_status = {
                    "name" : key,
                    "status" : status,
                    "data":"auto device",
                    "starttime" : starttime,
                    "endtime": None,
                    "iddevice" : "autoFanLivingRoom"
                }
                Env.database["statusdb"].insert(
					new_status
				)

                keyFan = "fan-living-room"
                new_status = {
                    "name" : keyFan,
                    "status" : status,
                    "data":"on device",
                    "starttime" : starttime,
                    "endtime": None,
                    "iddevice" : "fanLivingRoom"
                }
                Env.database["statusdb"].insert(
					new_status
				)

            if status == "off":
                GPIO.output(pinTemperatureHumidityRoom, GPIO.LOW)
                GPIO.output(pinFanLivingRoom, GPIO.LOW)
                endtime = datetime.datetime.utcnow() # Cap nhat thoi gian tat thiet bi

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
						"$set":
						 {
							 "endtime": endtime,
							 "status": status
						 }
					}
				)

                keyFan = "fan-living-room"
                finds = json.loads(
					dumps(
						Env.database["statusdb"]
							.find(
							{
								"name": keyFan
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

                f = finds["status"]
                Env.database["statusdb"].update(
					{
						"name": keyFan,
						"status": f
					},
					{
						"$set":
							{
								"endtime": endtime,
								"status": status
							}
					}
				)
