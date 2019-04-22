import tornado.web
from config import Env
import time
import datetime
from bson.json_util import dumps
import json
import RPi.GPIO as GPIO
import threading

class AutoClothesline(tornado.web.RequestHandler):

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
			while (1):
				Rain = GPIO.input(pinRainSensor)
				if (Rain == 1):
                    GPIO.output(pinClothesline, GPIO.HIGH)
				elif (Rain == 0):
					GPIO.output(pinClothesline, GPIO.LOW)		
				if stop_thread:
					print "exit"
					break

		if key == "auto-clothesline":
			if status == "on":
				stop_thread = False
				starttime = datetime.datetime.utcnow()
				threadAutoClothesline = threading.Thread(target=autoClothesline)
				threadAutoClothesline.start()
				new_status = {
					"name" : key,
					"status" : status,
					"data":"auto device",
					"starttime" : starttime,
					"endtime": None,
					"iddevice" : "autoClothesline"
				}
				Env.database["statusdb"].insert(new_status)	
			if status == "off":
				stop_thread = True
				endtime = datetime.datetime.utcnow()
				finds = json.loads(dumps(Env.database["statusdb"].find({"name":key},{"status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]
				
				f = finds["status"]
				Env.database["statusdb"].update({"name":key, "status":f},{"$set":{"endtime":endtime,"status":status}})