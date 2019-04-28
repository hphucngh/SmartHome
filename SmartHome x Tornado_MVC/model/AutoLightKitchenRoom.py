import time
import datetime
import json
import RPi.GPIO as GPIO
import threading
import LightsOnOff
import BaseHandler
from config import Env
from bson.json_util import dumps

class AutoLightKitchenRoom(BaseHandler.BaseHandler):
    @tornado.web.authenticated
	def post(self):
		global stop_thread
		pinMotionSensor = 23
		pinLightSensor = 24
		pinLightKitchenRoom = 17
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pinMotionSensor, GPIO.IN)
		GPIO.setup(pinLightSensor, GPIO.IN)
		GPIO.setup(pinLightKitchenRoom, GPIO.OUT)
		key = self.get_argument("key")
		status = self.get_argument("value")

		def autoLightKitchenRoom():
			while (1):
				MotionSensor = GPIO.input(pinMotionSensor)
				LightSensor = GPIO.input(pinLightSensor)
				if (LightSensor==1):
					if (MotionSensor==1):
						GPIO.output(pinLightKitchenRoom, GPIO.HIGH)
						time.sleep(1)
					elif MotionSensor==0:
						GPIO.output(pinLightKitchenRoom, GPIO.LOW)
						time.sleep(1)
				elif (LightSensor == 0):
					GPIO.output(pinLightKitchenRoom, GPIO.LOW)
				if stop_thread:
					break

		if key == "auto-light-kitchen-room":
			if status == "on":
				stop_thread = False
				starttime = datetime.datetime.utcnow()
				threadAutoLight = threading.Thread(target=autoLightKitchenRoom)
				threadAutoLight.start()
				new_status = {
					"name" : key,
					"status" : status,
					"data":"auto device",
					"starttime" : starttime,
					"endtime": None,
					"iddevice" : "autoLightKitchenRoom"
				}
				Env.database["statusdb"].insert(
					new_status
				)

				keyLight = "light-kitchen-room"
				iddevice = "lightKitchenRoom"
				new_status = {
					"name" : keyLight,
					"status" : status,
					"data":"auto device",
					"starttime" : starttime,
					"endtime": None,
					"iddevice" : iddevice
				}
				Env.database["statusdb"].insert(
					new_status
				)

			if status == "off":
				stop_thread = True
				GPIO.output(pinLightKitchenRoom, GPIO.LOW)
				endtime = datetime.datetime.utcnow()
				finds = json.loads(
					dumps(
						Env.database["statusdb"]
							.find(
							{
								"name":key
							},
							{
								"status":1,
								"_id":0
							}
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
							"status": status
						}
					}
				)

				keyLight = "light-kitchen-room"
				finds = json.loads(
					dumps(
						Env.database["statusdb"]
							.find(
							{
								"name": keyLight
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
					{"name": keyLight, "status": f},
					{
						"$set": {
							"endtime": endtime,
							"status": status
						}
					}
				)
